# RAG-based-PDF-QnA-System

## Introduction

An end-to-end **Retrieval-Augmented Generation (RAG)** system that enables semantic question answering over user-uploaded PDF documents. Built using **FastAPI**, **LangChain**, **ChromaDB** and **FAISS**, with support for **multi-user sessions**, **query caching**, and **containerized deployment**.

## 🔍 Key Features

- **Multi-PDF Support**: Upload and analyze one or more PDF documents.
- **Multi-User Sessions**: Isolated sessions using unique session IDs to prevent data leakage between users.
- **Asynchronous API**: FastAPI with `async` endpoints enables concurrent query handling.
- **Query Caching**: Reduce latency for repeated queries with in-memory cache.
- **Semantic Search**: Use FAISS to perform vector-based retrieval on document chunks.
- **Fully Containerized**: One-line setup with Docker and `docker-compose`.


## Steps: Start the host

### 1. Clone and Install

git clone https://github.com/yourusername/rag-pdf-qa.git

cd rag-pdf-qa

pip install -r requirements.txt

### 2. set .env

### 3. Run

uvicorn main:app --reload

### 4. Run with Docker

docker build -t rag-pdf-qa .

docker run -p 8000:8000 rag-pdf-qa


## API Usage:

### 1. Upload files:

curl -X POST http://127.0.0.1:8000/upload \\

  -F "file_path_1" \\
  
  -F "file_path_2"

return example:

{
  "messgae": "Upload Successful!",
  
  "session_id": "2f3cd581-c3d1-4e01-8672-6b3e88283900"
}

### 2. Ask questions:

curl -X POST http://127.0.0.1:8000/ask \\

  -H "Content-Type: application/json" \\
  
  -d '{
    "session_id": "2f3cd581-c3d1-4e01-8672-6b3e88283900",
    "question": "What is the main conclusion of the document?"
  }'

return example:

{"response":" The main conclusion of the document is that Goldilocks trespassed in the bears' home, consumed their food and personal belongings, and ultimately caused harm and distress to the bear family."}

