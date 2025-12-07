# backend/main.py

import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_pipeline import RAGPipeline
from fastapi.middleware.cors import CORSMiddleware
# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# FastAPI app setup
app = FastAPI(title="RAG Q&A")
# Configure CORS for frontend integration
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
# Request models
class AskRequest(BaseModel):
    """
    Schema for POST /ask request.
    
    Attributes:
        question (str): The user question to be answered by the RAG pipeline.
    """
    question: str
class Question(BaseModel):
    question: str

# Variables d'environnement
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store")
DOCS_PATH = os.getenv("DOCS_PATH", "./docs")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Pipeline singleton
pipeline = RAGPipeline(persist_directory=VECTOR_STORE_PATH, groq_api_key=GROQ_API_KEY)
# Startup event
@app.on_event("startup")
def startup_event():
    """
    Check if the vector store is initialized when the FastAPI app starts.
    Logs a message if ingestion is required.
    """
    if not pipeline.is_initialized():
        logger.info("Vector store not initialized. Ingestion is required before asking questions.")

# API endpoints
@app.post("/ask")
def ask_question(payload: Question):
    """
    Endpoint to ask a question to the RAG pipeline.

    Args:
        payload (Question): JSON payload containing the user question.

    Returns:
        dict: Dictionary containing the answer and the sources.

    Raises:
        HTTPException: If an error occurs during question answering.
    """
    try:
        answer = pipeline.answer_question(payload.question)
        return {"answer": answer}
    except Exception as e:
        logger.error(f"/ask error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    """
    Health check endpoint.

    Returns:
        dict: Status of the API and whether the vector store is initialized.
              {
                  "status": "ok",
                  "vector_store_initialized": bool
              }
    """
    return {"status": "ok", "vector_store_initialized": pipeline.is_initialized()}
