import os
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from sentence_transformers import SentenceTransformer
import chromadb
from langchain_groq import ChatGroq


class RAGPipeline:
    """
    Retrieval-Augmented Generation (RAG) Pipeline.

    This class handles:
    - Loading and splitting documents
    - Creating embeddings with SentenceTransformers
    - Storing embeddings in Chroma vector store
    - Querying a Groq LLM using the stored embeddings

    Attributes:
        persist_directory (str): Directory to store the Chroma vector database.
        model (SentenceTransformer): Model used to create embeddings.
        chroma_client (PersistentClient): Chroma database client.
        collection (Collection): Chroma collection for document embeddings.
        llm (ChatGroq): Groq LLM for answering questions.
    """
    def __init__(self, persist_directory="vectorstore", groq_api_key=os.getenv("GROQ_API_KEY")
):
        """
        Initialize the RAG pipeline.

        Args:
            persist_directory (str): Directory to persist vector store.
            groq_api_key (str): API key for Groq LLM. Reads from environment if not provided.

        Raises:
            ValueError: If GROQ_API_KEY is not provided.
        """
        self.persist_directory = persist_directory
        
        # Embedding model
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Vector DB
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.chroma_client.get_or_create_collection(
            name="docs",
            metadata={"hnsw:space": "cosine"},
        )

        # Groq LLM
        if not groq_api_key:
            raise ValueError("Missing GROQ_API_KEY")
        self.llm = ChatGroq(api_key=groq_api_key, model="llama-3.1-8b-instant")


    def load_documents(self, folder_path):
        """
        Load documents from a folder, supporting PDF, TXT, and Markdown formats.

        Args:
            folder_path (str): Path to the folder containing documents.

        Returns:
            list: List of loaded Document objects.
        """
        docs = []
        for root, _, files in os.walk(folder_path):
            for f in files:
                path = os.path.join(root, f)
                if f.endswith(".pdf"):
                    loader = PyPDFLoader(path)
                elif f.endswith(".txt"):
                    loader = TextLoader(path)
                elif f.endswith(".md"):
                    loader = UnstructuredMarkdownLoader(path)
                else:
                    continue
                docs.extend(loader.load())
        return docs


    def split_documents(self, docs):
        """
        Split documents into chunks for embedding.

        Args:
            docs (list): List of Document objects.

        Returns:
            list: List of chunked Document objects.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        return splitter.split_documents(docs)


    def create_embeddings(self, docs):
        """
        Create embeddings for documents and add them to the Chroma vector store.

        Args:
            docs (list): List of chunked Document objects.
        """
        texts = [d.page_content for d in docs]
        embeddings = self.model.encode(texts).tolist()
        for i, (doc, emb) in enumerate(zip(docs, embeddings)):
            self.collection.add(
                ids=[f"chunk-{i}"],
                documents=[doc.page_content],
                embeddings=[emb],
                metadatas=[{"source": doc.metadata.get("source", "unknown")}],
            )


    def query(self, question: str, k=3):
        """
        Query the vector store to retrieve relevant documents.

        Args:
            question (str): User question.
            k (int): Number of top results to retrieve.

        Returns:
            tuple: (documents, sources) where `documents` is a list of text chunks, 
                   and `sources` is a list of corresponding source filenames.
        """
        embedding = self.model.encode(question).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=k
        )

        docs = results["documents"][0]
        sources = [meta.get("source", "unknown") for meta in results["metadatas"][0]]

        return docs, sources


    def is_initialized(self):
        """
        Check if the vector store has been initialized and contains data.

        Returns:
            bool: True if the collection contains embeddings, False otherwise.
        """
        try:
            return bool(self.collection.count())
        except:
            return False


    def answer_question(self, question: str, k=3):
        """
        Answer a question using the RAG approach: 
        retrieve relevant documents and query the Groq LLM.

        Args:
            question (str): User question.
            k (int): Number of top documents to retrieve for context.

        Returns:
            dict: Dictionary containing the answer and the sources.
                  {
                      "answer": str,
                      "sources": list[str]
                  }
        """

        docs, sources = self.query(question, k=k)
        context = "\n".join(docs)

        prompt = (
            "Tu es un assistant qui répond STRICTEMENT en te basant sur le contexte.\n\n"
            f"Question: {question}\n\n"
            f"Contexte:\n{context}\n\n"
            "Réponse :"
        )

        response = self.llm.invoke(prompt)

        return {"answer": response.content, "sources": sources}
