from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def load_and_split_pdf(file_path, doc_id):

    # ✅ Check if file exists (IMPORTANT FIX)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # ✅ Load PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # ✅ Handle empty PDF
    if not documents:
        raise ValueError("No content found in PDF")

    # ✅ Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    docs = splitter.split_documents(documents)

    # ✅ Add metadata
    for i, doc in enumerate(docs):
        doc.metadata["source"] = os.path.basename(file_path)  # cleaner UI
        doc.metadata["doc_id"] = doc_id
        doc.metadata["chunk_id"] = i  # optional but useful

    return docs