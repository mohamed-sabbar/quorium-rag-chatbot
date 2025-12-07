# backend/main.py

import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_pipeline import RAGPipeline
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Q&A")
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class AskRequest(BaseModel):
    question: str
class Question(BaseModel):
    question: str

# Variables d'environnement
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store")
DOCS_PATH = os.getenv("DOCS_PATH", "./docs")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Pipeline singleton
pipeline = RAGPipeline(persist_directory=VECTOR_STORE_PATH, groq_api_key=GROQ_API_KEY)

@app.on_event("startup")
def startup_event():
    if not pipeline.is_initialized():
        logger.info("Vector store not initialized. Ingestion is required before asking questions.")

@app.post("/ask")
def ask_question(payload: Question):
    try:
        answer = pipeline.answer_question(payload.question)
        return {"answer": answer}
    except Exception as e:
        logger.error(f"/ask error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok", "vector_store_initialized": pipeline.is_initialized()}
