#/backend/ingest.py
import os
from rag_pipeline import RAGPipeline

if __name__ == "__main__":
    # Retrieve folder paths from environment variables with default values
    DOCUMENTS_FOLDER = os.getenv("DOCS_PATH", "/app/data/docs")
    VECTOR_STORE_FOLDER = os.getenv("VECTOR_STORE_PATH", "/app/vector_store")
    # Initialize the RAG pipeline
    # RAGPipeline will automatically read the GROQ_API_KEY from the environment
    rag = RAGPipeline(persist_directory=VECTOR_STORE_FOLDER)
    #  Load documents
    print("Loading documents...")
    docs = rag.load_documents(DOCUMENTS_FOLDER)
    print(f"Loaded {len(docs)} raw documents")
    # 2️ Split documents into chunks
    print("Splitting documents...")
    chunks = rag.split_documents(docs)
    print(f"Generated {len(chunks)} chunks")

    # 3️ Create embeddings and save them to the vector store
    print("Creating embeddings and saving vector store...")
    rag.create_embeddings(chunks)
    # End of ingestion
    print("Ingestion complete!")
