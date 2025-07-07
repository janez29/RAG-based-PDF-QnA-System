from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.init_rag import init_rag
import uuid
import os,shutil
from set_cahce import set_cache, get_cache, is_cache

load_dotenv()
app = FastAPI()

# Set environment variables
model_dir = os.getenv("MODEL_PATH")
file_name = os.getenv("FILE_NAME")
max_session = int(os.getenv("MAX_SESSION"))
chunk_size = int(os.getenv("CHUNK_SIZE"))
chunk_overlap = int(os.getenv("CHUNK_OVERLAP"))

# Design FastAPI
class query(BaseModel):
    session_id: str
    question: str

@app.post("/upload")
async def upload(files: list[UploadFile] = File(...)):
    session_id = str(uuid.uuid4())
    session_dir = f"./temp/{session_id}"
    os.makedirs(session_dir, exist_ok = True)
    file_paths = []
    for file in files:
        file_path = os.path.join(session_dir, file.filename)
        with open(file_path,'wb') as f:
            shutil.copyfileobj(file.file,f)
        file_paths.append(file_path)
    try:
        qa_chain = init_rag(file_paths,model_dir,file_name,chunk_size,chunk_overlap)
        set_cache(session_id, qa_chain, max_session)
        return {"messgae":"Upload Successful!", "session_id": session_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/ask")
async def ask(request: query):
    if not is_cache(request.session_id):
        return JSONResponse(status_code=500, content={"error","session_id not found!"})
    try:
        RAG = get_cache(request.session_id)
        result = RAG.invoke({"query":request.question})
        return {"response": result["result"]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
