#/backend/ingest.py
import os
from rag_pipeline import RAGPipeline

if __name__ == "__main__":
    DOCUMENTS_FOLDER = os.getenv("DOCS_PATH", "/app/data/docs")
    VECTOR_STORE_FOLDER = os.getenv("VECTOR_STORE_PATH", "/app/vector_store")

    rag = RAGPipeline(persist_directory=VECTOR_STORE_FOLDER)

    print("📄 Loading documents...")
    docs = rag.load_documents(DOCUMENTS_FOLDER)
    print(f"Loaded {len(docs)} raw documents")

    print("✂️ Splitting documents...")
    chunks = rag.split_documents(docs)
    print(f"Generated {len(chunks)} chunks")

    print("🧠 Creating embeddings and saving vector store...")
    rag.create_embeddings(chunks)
  
    print("✅ Ingestion complete!")
