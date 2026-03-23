import os
import shutil
from langchain_community.vectorstores import FAISS

VECTOR_PATH = "vector_store"


def create_vector_store(docs, embedding_model):
    if os.path.exists(VECTOR_PATH):
        db = FAISS.load_local(VECTOR_PATH, embedding_model, allow_dangerous_deserialization=True)
        db.add_documents(docs)
    else:
        db = FAISS.from_documents(docs, embedding_model)

    db.save_local(VECTOR_PATH)
    return db


def load_vector_store(embedding_model):
    if not os.path.exists(VECTOR_PATH):
        return None
    return FAISS.load_local(VECTOR_PATH, embedding_model, allow_dangerous_deserialization=True)


def delete_document(doc_id, embedding_model):
    db = load_vector_store(embedding_model)
    if db is None:
        return

    docs = list(db.docstore._dict.values())

    # remove only selected doc
    filtered_docs = [
        doc for doc in docs
        if doc.metadata.get("doc_id") != doc_id
    ]

    # reset vector store
    import shutil
    if os.path.exists(VECTOR_PATH):
        shutil.rmtree(VECTOR_PATH)

    if filtered_docs:
        new_db = FAISS.from_documents(filtered_docs, embedding_model)
        new_db.save_local(VECTOR_PATH)