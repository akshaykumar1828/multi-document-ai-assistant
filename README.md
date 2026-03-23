# 🚀 Multi-Document AI Assistant (RAG + LangChain)

A basic intelligent AI-powered system that allows users to upload multiple PDFs and interact with them through a conversational interface. The system uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers.

---

## 🔥 Features

* 📄 Upload multiple PDF documents
* 💬 Chat with documents (like ChatGPT)
* 🧠 Context-aware answers using RAG
* 🔍 Semantic search using FAISS
* 📊 Summarization of documents
* 🔄 Multi-document reasoning (answers across PDFs)
* 🧾 Source tracking (file + page reference)
* 🗑️ Delete documents (updates vector store)
* 🧠 Chat history support

---

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **Frontend:** Streamlit
* **LLM:** Groq (LLaMA 3.1)
* **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
* **Vector DB:** FAISS
* **Framework:** LangChain

---

## 🧠 Architecture (RAG Pipeline)

```text
User Query
    ↓
Embedding
    ↓
FAISS Vector Search
    ↓
Relevant Document Chunks
    ↓
LLM (Groq)
    ↓
Final Answer
```

---

## 📂 Project Structure

```text
multi-document-ai-assistant/
│
├── app/
│   ├── main.py              # FastAPI backend
│   ├── streamlit_app.py    # Streamlit frontend
│
├── rag/
│   ├── loader.py           # PDF loading & chunking
│   ├── embeddings.py      # Embedding model
│   ├── vector_store.py    # FAISS operations
│   ├── pipeline.py        # RAG logic
│
├── data/                  # Uploaded PDFs
├── vector_store/          # FAISS index
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions



---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

### 5️⃣ Run Backend (FastAPI)

```bash
uvicorn app.main:app --reload
```

---

### 6️⃣ Run Frontend (Streamlit)

```bash
streamlit run app/streamlit_app.py
```

---

## 💡 Usage

1. Upload one or more PDF files
2. Ask questions like:

   * “Summarize the document”
   * “What topics are covered?”
   * “Explain modulation”
3. Get answers with sources

---

## 🧠 Key Features Explained

### 🔹 Multi-Document Retrieval

The system retrieves relevant chunks across multiple PDFs and combines them for better answers.

---

### 🔹 Query Intent Handling

* Detects summary queries
* Handles general vs specific questions
* Avoids hallucination

---

### 🔹 Chat Memory

Maintains previous conversation context for better responses.

---

### 🔹 Vector Store Management

* Add documents dynamically
* Delete documents and rebuild FAISS index

---



## 🔮 Future Improvements

* 🔍 Hybrid search (BM25 + embeddings)
* 📌 Highlight answers in PDF
* 🌐 Deployment (Render / AWS)
* 🔐 User authentication
* ⚡ Streaming responses (typing effect)



---

