import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import LlamaCpp
from huggingface_hub import hf_hub_download

def init_rag(pdf_path,model_dir,file_name, chunk_size, chunk_overlap):
    # Step 1: Load PDF
    docs = []
    model_path = model_dir + '/' + file_name
    for file in pdf_path:
        loader = PyPDFLoader(file)
        docs.extend(loader.load())

    # Step 2: Split
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    splitted_docs = splitter.split_documents(docs)

    # Step 3: Embed
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(splitted_docs, embedding=embeddings)

    # Step 4: Download the model and use RAG
    if not os.path.exists(model_path):
        model_id = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
        filename = file_name
        local_path = hf_hub_download(
            repo_id=model_id,
            filename=filename,
            local_dir=model_dir,
            local_dir_use_symlinks=False
        )
        print(f"Model downloaded to: {local_path}")

    llm = LlamaCpp(
        model_path=model_path,
        n_ctx=2048,
        n_threads=6,          # 根据你的 Mac 调整
        n_gpu_layers=20,      # 使用 Metal 加速
        use_mlock=True
    )

    # Step 5: return QA chain
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
    return qa_chain
