from fastapi import FastAPI, UploadFile, File
import shutil
import os
import uuid

from rag.loader import load_and_split_pdf
from rag.embeddings import get_embedding_model
from rag.vector_store import create_vector_store, delete_document
from rag.pipeline import answer_query

app = FastAPI()

UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

embedding_model = get_embedding_model()

# global memory
chat_history = []


@app.get("/")
def home():
    return {"message": "RAG API Running 🚀"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # ✅ Ensure folder exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # ✅ Safe file path
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # ✅ Save file properly
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ✅ Double check file exists
        if not os.path.exists(file_path):
            raise Exception("File was not saved properly")

        doc_id = str(uuid.uuid4())

        # ✅ Load AFTER saving
        docs = load_and_split_pdf(file_path, doc_id)

        create_vector_store(docs, embedding_model)

        return {"doc_id": doc_id}

    except Exception as e:
        return {"error": str(e)}


@app.get("/query")
def query(q: str):
    global chat_history

    result = answer_query(q, chat_history)

    chat_history.append((q, result["answer"]))

    return result


@app.delete("/delete/{doc_id}")
def delete(doc_id: str):
    global chat_history

    delete_document(doc_id, embedding_model)

    # also clear history related to that doc
    chat_history = []

    return {"message": "Deleted successfully"}