import os
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader
from sentence_transformers import SentenceTransformer
import chromadb
from langchain_groq import ChatGroq


class RAGPipeline:
    def __init__(self, persist_directory="vectorstore", groq_api_key=None):
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
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        return splitter.split_documents(docs)


    def create_embeddings(self, docs):
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
        embedding = self.model.encode(question).tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=k
        )

        docs = results["documents"][0]
        sources = [meta.get("source", "unknown") for meta in results["metadatas"][0]]

        return docs, sources


    def is_initialized(self):
        try:
            return bool(self.collection.count())
        except:
            return False


    def answer_question(self, question: str, k=3):

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
