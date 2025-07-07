# RAG-based-PDF-QnA-System

## Introduction

This is light-weight PDF Q&A applications using Retrieval-Augmented Generation (RAG). It use Mistral-7B as a backbone and run LLM locally. It supports update single or mutiple PDFs at the same time, and the chunk size and overlap size can be customized. It adopts a session-based cache system with LRU eviction. The project also provides a dockerized version for easy deployment. 

## Tech

FastAPI, LangChain, Docker, LlamaCPP, ChromaDB, HuggingFace

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

curl -X POST http://127.0.0.1:8000/upload \
  -F "file_path_1" \
  -F "file_path_2"

return example:

{
  "messgae": "Upload Successful!",
  "session_id": "2f3cd581-c3d1-4e01-8672-6b3e88283900"
}

### 2. Ask questions:

curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "2f3cd581-c3d1-4e01-8672-6b3e88283900",
    "question": "What is the main conclusion of the document?"
  }'


