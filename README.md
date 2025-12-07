# RAG Q&A Chatbot 🤖

A Retrieval-Augmented Generation (RAG) application that answers questions based on provided documents. Built with FastAPI (backend), Next.js (frontend), LangChain, and Docker.

---

## 📋 Table of Contents

1. [Features](#-features)
2. [Architecture](#-architecture)
3. [Requirements](#-requirements)
4. [Installation](#-installation)
5. [Usage](#-usage)
6. [Project Structure](#-project-structure)
7. [API Documentation](#-api-documentation)
8. [Docker Commands](#-docker-commands)
9. [Configuration](#-configuration)
10. [Testing](#-testing)
11. [Troubleshooting](#-troubleshooting)
12. [Performance](#-performance)
13. [Technologies](#-technologies)
14. [Security](#-security)
15. [Future Improvements](#-future-improvements)

---

## 🚀 Features

- ✅ **Document Ingestion**: Support for PDF, TXT, and Markdown files
- ✅ **Complete RAG Pipeline**: Chunking, embeddings, vector search
- ✅ **FastAPI Backend**: RESTful API with automatic documentation
- ✅ **Next.js Frontend**: Modern chat interface with React 19 and TypeScript
- ✅ **Docker Ready**: Complete orchestration with docker-compose
- ✅ **Source Citations**: Displays source documents for answers
- ✅ **GROQ LLM Integration**: GROQ API integration for fast inference
- ✅ **Persistent Vector Store**: Chroma for embedding storage

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────┐
│                   RAG Q&A APPLICATION                      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────────┐      ┌──────────────────────┐  │
│  │  Frontend (Next.js)  │      │  Backend (FastAPI)   │  │
│  │  Port 3000           │◄────►│  Port 8000           │  │
│  │                      │      │                      │  │
│  │  - Chat Interface    │      │  - /ask endpoint     │  │
│  │  - React 19          │      │  - /health check     │  │
│  │  - Tailwind CSS      │      │  - API docs          │  │
│  └──────────────────────┘      └──────────────────────┘  │
│                                         ▲                  │
│                                         │                  │
│                    ┌────────────────────┴─────────┐        │
│                    ▼                              ▼        │
│        ┌─────────────────────┐      ┌──────────────────┐  │
│        │  LangChain RAG      │      │  Chroma Vector   │  │
│        │  Pipeline           │◄────►│  Store           │  │
│        │                     │      │  (Persistent)    │  │
│        │  - Document Loader  │      │                  │  │
│        │  - Text Splitter    │      │  - Embeddings    │  │
│        │  - Query/Retrieval  │      │  - Similarity    │  │
│        └─────────────────────┘      │    Search        │  │
│                │                    └──────────────────┘  │
│                ▼                                           │
│        ┌──────────────────────────────────────┐           │
│        │  Sentence Transformers (MiniLM)     │           │
│        │  Model: all-MiniLM-L6-v2            │           │
│        └──────────────────────────────────────┘           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 📋 Requirements

Before starting, ensure you have:

- **Docker Desktop** installed and running
- **4GB+ RAM** available
- **Internet connection** (for downloading models)
- **GROQ API Key** (free at https://console.groq.com/keys)

---

## 📦 Installation

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd quorium-rag-chatbot
```

### Step 2: Configure GROQ API Key

The GROQ API key is already embedded in the `docker-compose.yml` file:

```yaml
environment:
  - GROQ_API_KEY=${GROQ_API_KEY:-}
```

> ⚠️ **Important**: Replace this key with your own from https://console.groq.com/keys

To change the key, edit `docker-compose.yml`:

```yaml
services:
  backend:
    environment:
      - GROQ_API_KEY=your_new_api_key_here
```

### Step 3: Prepare Documents

Place your documents in the `backend/data/docs/` folder:

```bash
# Create the folder if it doesn't exist
mkdir -p ./backend/data/docs

# Copy your documents
cp /path/to/your/documents/* ./backend/data/docs/
```

**Supported formats**:

- 📄 PDF
- 📝 TXT
- 📋 Markdown (.md)

### Step 4: Build Docker Images

Make the script executable and build the images:

```bash
# Make script executable (Linux/Mac/WSL)
chmod +x docker.sh

# Build Docker images
./docker.sh build
```

This will:

- Build the backend Python container
- Build the frontend Node.js container
- Download all dependencies
- **Time**: 3-5 minutes (first time)

### Step 5: Start Services

```bash
# Start services in the background
./docker.sh up
```

Services will be available at:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Step 6: Ingest Documents

Open a **new terminal** and run:

```bash
# Ingest documents
./docker.sh ingest
```

You will see:

```
📄 Loading documents...
Loaded 10 raw documents

✂️ Splitting documents...
Generated 250 chunks

🧠 Creating embeddings and saving vector store...

✅ Ingestion complete!
```

**Estimated time**: 30-90 seconds depending on document size

### Step 7: Use the Application

1. Open your browser: **http://localhost:3000**
2. Type your question in the chat interface
3. Get answers based on your documents with sources

---

## 💻 Usage

### Via Web Interface

1. Go to http://localhost:3000
2. Enter your question
3. Get a response based on the ingested documents
4. View the source documents used

### Via REST API

#### Ask a Question

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

**Response**:

```json
{
  "answer": "Based on the provided documents, this document...",
  "sources": ["document1.pdf", "document2.txt"]
}
```

#### Health Check

```bash
curl http://localhost:8000/health
```

**Response**:

```json
{
  "status": "ok",
  "vector_store_initialized": true
}
```

#### Interactive API Documentation

Visit: http://localhost:8000/docs

You will see the Swagger UI documentation with all endpoints

---

## 📁 Project Structure

```
quorium-rag-chatbot/
│
├── 📄 README.md                    # This file
├── 📄 docker-compose.yml           # Docker orchestration
├── 📄 docker.ps1                   # PowerShell script (optional)
├── 📄 docker.sh                    # Bash script
│
├── 📁 backend/
│   ├── 📄 main.py                  # FastAPI application
│   ├── 📄 rag_pipeline.py          # RAG pipeline logic
│   ├── 📄 ingest.py                # Document ingestion script
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 Dockerfile               # Backend container
│   │
│   ├── 📁 data/
│   │   └── 📁 docs/                # Your documents (PDF, TXT, MD)
│   │
│   └── 📁 vector_store/            # Chroma vector database
│       ├── chroma.sqlite3
│       └── [collections]/
│
├── 📁 frontend/
│   ├── 📄 package.json             # Node.js dependencies
│   ├── 📄 tsconfig.json            # TypeScript configuration
│   ├── 📄 next.config.ts           # Next.js configuration
│   ├── 📄 tailwind.config.js       # Tailwind configuration
│   ├── 📄 Dockerfile               # Frontend container
│   │
│   ├── 📁 app/
│   │   ├── 📄 layout.tsx           # Main layout
│   │   ├── 📄 page.tsx             # Home page
│   │   ├── 📄 Chat.tsx             # Chat component
│   │   ├── 📄 globals.css          # Global styles
│   │   └── 📄 page.module.css      # Component styles
│   │
│   └── 📁 public/
│       └── 📄 style.css            # Additional styles
```

---

## 🔌 API Documentation

### Available Endpoints

#### 1. POST /ask

Ask the chatbot a question

**Request**:

```json
{
  "question": "What is the conclusion of the document?"
}
```

**Response**:

```json
{
  "answer": "Based on the documents...",
  "sources": ["document.pdf"]
}
```

#### 2. GET /health

Check application status

**Response**:

```json
{
  "status": "ok",
  "vector_store_initialized": true
}
```

#### 3. GET /docs

Interactive Swagger UI Documentation

---

## 🎮 Docker Commands

All commands use the `docker.sh` script:

```bash
# Build Docker images
./docker.sh build

# Start services in background
./docker.sh up

# Stop services
./docker.sh down

# Ingest documents
./docker.sh ingest

# Display logs in real-time
./docker.sh logs

# General usage
./docker.sh {build|up|down|ingest|logs}
```

### What Each Command Does

**`./docker.sh build`**

- Builds the backend Python container (Python 3.11-slim)
- Builds the frontend Node.js container (Node.js 20.11.1)
- Downloads and installs all dependencies
- Time: 3-5 minutes (first time)

**`./docker.sh up`**

- Starts all containers in the background
- Services are ready for use after a few seconds
- Shows output in the terminal

**`./docker.sh down`**

- Stops all running containers
- Removes container networks
- Data in vector_store is preserved

**`./docker.sh ingest`**

- Runs the document ingestion pipeline
- Loads documents from `backend/data/docs/`
- Splits into chunks (800 chars, 200 overlap)
- Generates embeddings using sentence-transformers
- Stores in Chroma vector database
- Time: 30-90 seconds

**`./docker.sh logs`**

- Shows real-time logs from all services
- Press Ctrl+C to stop
- Useful for debugging

---

## 🔧 Configuration

### Change GROQ API Key

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    environment:
      - GROQ_API_KEY=your_new_api_key_here
```

### Customize Ports

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8080:8000" # Backend on port 8080

  frontend:
    ports:
      - "3001:3000" # Frontend on port 3001
```

### Adjust Document Chunking

Edit `backend/rag_pipeline.py`:

```python
def split_documents(self, docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,      # Size of chunks in characters
        chunk_overlap=100    # Overlap between chunks
    )
    return splitter.split_documents(docs)
```

### Change Embedding Model

Edit `backend/rag_pipeline.py`:

```python
self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# Or use other models: "all-mpnet-base-v2", "all-roberta-large-v1"
```

---

## 🧪 Testing

### Quick Test

```bash
# 1. Build images
./docker.sh build

# 2. Start services
./docker.sh up

# 3. Wait a few seconds
sleep 10

# 4. Ingest documents
./docker.sh ingest

# 5. View logs
./docker.sh logs
```

### Test with curl

```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What does this document explain?"}'
```

### Manual Testing

1. Open http://localhost:3000
2. Type a question
3. Check that the response appears
4. Verify source documents are shown

---

## 🐛 Troubleshooting

### ❌ Error: "Docker is not running"

```bash
# Check Docker installation
docker --version

# Start Docker Desktop (macOS/Windows)
# Or start Docker daemon (Linux)
```

### ❌ Error: "Port 3000/8000 already in use"

```bash
# Option 1: Stop the other service
# Find what's using the port and stop it

# Option 2: Change ports in docker-compose.yml
# Edit the ports section for backend/frontend
```

### ❌ Error: "Vector store not initialized"

```bash
# Run ingestion
./docker.sh ingest

# Verify documents exist
ls -la ./backend/data/docs/
```

### ❌ First query is very slow

This is normal! The first query downloads the LLM model (~1GB).
Subsequent queries will be faster (2-5 seconds).

### ❌ No documents were ingested

```bash
# Check if documents are in the right folder
ls -la ./backend/data/docs/

# Verify supported formats (PDF, TXT, MD)

# Try ingestion again
./docker.sh ingest

# View logs
./docker.sh logs
```

### ❌ Answers are not relevant

- Check if documents are loaded correctly
- Documents must be readable text (not scanned images)
- Try with more specific questions

---

## 📊 Performance

| Metric                 | Duration/Size                  |
| ---------------------- | ------------------------------ |
| **Ingestion**          | 30-90 sec per 100 pages        |
| **First query**        | 15-30 sec (model download)     |
| **Subsequent queries** | 2-5 seconds                    |
| **RAM Memory**         | ~2GB backend + ~500MB frontend |
| **Vector storage**     | ~10MB per 1000 chunks          |

---

## 📋 Technologies

### Backend

- **FastAPI** - Asynchronous web framework
- **LangChain** - RAG framework
- **Chroma** - Vector database
- **Sentence-Transformers** - Embedding model
- **GROQ API** - Cloud LLM service
- **Python 3.11** - Language

### Frontend

- **Next.js 16** - React SSR framework
- **React 19** - UI library
- **TypeScript 5** - Static typing
- **Tailwind CSS 4** - CSS framework
- **Node.js 20** - JavaScript runtime

### Infrastructure

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

---

## 🔐 Security

### ⚠️ Important Notes

- **No authentication** (development environment)
- **CORS enabled** for localhost only
- **API key in docker-compose.yml** - Keep it secret!

### 🛡️ For Production

1. Add authentication (JWT, OAuth2)
2. Restrict CORS to authorized domains
3. Use secrets management (Vault, AWS Secrets Manager)
4. Enable HTTPS/TLS
5. Add rate limiting
6. Validate user input
7. Implement secure logging

---

## 🚀 Future Improvements

- [ ] User authentication
- [ ] Conversation history
- [ ] Support for DOCX, PPTX files
- [ ] Semantic caching
- [ ] Streaming responses
- [ ] Multi-language support
- [ ] Web search integration
- [ ] Document management UI

---

## 👤 Author

- **Project**: Quorium RAG Chatbot
- **Branch**: challenge/sabbar-rag-chatbot
- **Date**: December 2025

---

## 📄 License

This project was created for the Quorium AI Engineer Trainee coding challenge.

---

## 📞 Support

For issues:

1. Check the **Troubleshooting** section
2. View logs: `./docker.sh logs`
3. Read API documentation: http://localhost:8000/docs

**Good luck! 🎉**
