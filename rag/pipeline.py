import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from rag.embeddings import get_embedding_model
from rag.vector_store import load_vector_store

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

embedding_model = get_embedding_model()


def is_summary_query(query):
    keywords = ["summary", "summarize", "overview", "explain document"]
    return any(word in query.lower() for word in keywords)


def is_greeting(query):
    return query.lower().strip() in ["hi", "hello", "hey"]


def answer_query(query, chat_history=None):
    db = load_vector_store(embedding_model)

    # -----------------------
    # No documents case
    # -----------------------
    if db is None:
        return {
            "answer": "Please upload documents first.",
            "sources": []
        }

    # -----------------------
    # Greeting handling
    # -----------------------
    if is_greeting(query):
        return {
            "answer": "Hi! Ask me anything about your uploaded documents 😊",
            "sources": []
        }

    # -----------------------
    # SUMMARY MODE
    # -----------------------
    if is_summary_query(query):
        docs = db.similarity_search("", k=5)
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""
You are an AI assistant.

Summarize the given content clearly and naturally.

Instructions:
Instructions:
- Extract topics from ALL provided content
- Combine information from multiple documents if present
- Do NOT ignore any document
- DO NOT add any extra information on your own
- Keep answer structured (bullet points preferred)

Content:
{context}
"""
        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "sources": []
        }

    # -----------------------
    # NORMAL RAG QA
    # -----------------------
    # -----------------------
# SMART RETRIEVAL
# -----------------------

    # detect broad queries
    broad_keywords = ["topics", "discussed", "overview", "contents"]

    if any(word in query.lower() for word in broad_keywords):
        docs = db.similarity_search("", k=5)   # 🔥 force retrieval
    else:
        docs = db.similarity_search(query, k=3)

    # remove duplicates
    seen = set()
    unique_docs = []
    for doc in docs:
        text = doc.page_content.strip()
        if text not in seen:
            seen.add(text)
            unique_docs.append(doc)

    context = "\n\n".join([doc.page_content for doc in unique_docs])

    # chat history context
    history_text = ""
    if chat_history:
        for q, a in chat_history[-3:]:
            history_text += f"User: {q}\nAssistant: {a}\n"

    prompt = f"""
You are a helpful AI assistant.

Chat History:
{history_text}

Context:
{context}

Instructions:
- Use the context as the primary source of truth
- If relevant, use chat history to maintain conversation flow
- Do NOT make up information outside the context
- If the answer is not in the context, say: "Not found in documents"
- Answer clearly, naturally, and concisely

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": [
            {
                "file": doc.metadata.get("source"),
                "page": doc.metadata.get("page", "N/A")
            }
            for doc in unique_docs[:2]
        ]
    }