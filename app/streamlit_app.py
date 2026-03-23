import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Multi-Document AI Chat", layout="wide")

st.title("💬 Multi-Document AI Chat")

# ---------------- SESSION ----------------
if "docs" not in st.session_state:
    st.session_state.docs = {}

if "history" not in st.session_state:
    st.session_state.history = []

if "uploaded_files_cache" not in st.session_state:
    st.session_state.uploaded_files_cache = set()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("📤 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["pdf"],
        accept_multiple_files=True,
        key="file_uploader"
    )

    if uploaded_files:
        for file in uploaded_files:

            # ✅ Prevent re-upload loop
            if file.name not in st.session_state.uploaded_files_cache:

                files = {"file": (file.name, file.getvalue(), "application/pdf")}
                
                try:
                    res = requests.post(f"{API_URL}/upload", files=files)
                except Exception as e:
                    st.error("❌ Backend not reachable")
                    continue

                if res.status_code == 200:
                    try:
                        data = res.json()
                    except:
                        st.error("❌ Invalid response from server")
                        st.text(res.text)
                        continue

                    # ✅ SAFE CHECK (IMPORTANT FIX)
                    if "doc_id" in data:
                        st.session_state.docs[file.name] = data["doc_id"]
                        st.session_state.uploaded_files_cache.add(file.name)
                        st.success(f"{file.name} uploaded")
                    else:
                        st.error("❌ Upload failed")
                        st.text(data)

                else:
                    st.error(f"❌ Server error: {res.status_code}")
                    st.text(res.text)

    st.divider()
    st.header("📂 Documents")

    for name, doc_id in list(st.session_state.docs.items()):
        col1, col2 = st.columns([4, 1])

        col1.write(name)

        if col2.button("❌", key=f"delete_{name}"):

            try:
                res = requests.delete(f"{API_URL}/delete/{doc_id}")
            except:
                st.error("❌ Backend not reachable")
                continue

            if res.status_code == 200:
                del st.session_state.docs[name]
                st.session_state.uploaded_files_cache.discard(name)
                st.session_state.history = []

                st.success(f"{name} deleted")
                st.rerun()

            else:
                st.error("❌ Failed to delete document")

    # clear chat
    if st.button("🧹 Clear Chat"):
        st.session_state.history = []

# ---------------- CHAT INPUT ----------------
query = st.chat_input("Ask anything about your documents...")

if query:
    try:
        res = requests.get(f"{API_URL}/query", params={"q": query})
        data = res.json()
    except:
        st.error("❌ Failed to connect to backend")
        data = {"answer": "Error occurred", "sources": []}

    # prevent duplicate messages
    if not st.session_state.history or st.session_state.history[-1][0] != query:
        st.session_state.history.append(
            (query, data.get("answer", ""), data.get("sources", []))
        )

# ---------------- CHAT DISPLAY ----------------
for q, a, sources in st.session_state.history:

    # USER (RIGHT)
    st.markdown(f"""
    <div style='display:flex; justify-content:flex-end'>
        <div style='background:#E3F2FD; color:black;
                    padding:10px; border-radius:12px;
                    max-width:55%; margin:5px'>
            {q}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # AI (LEFT)
    st.markdown(f"""
    <div style='display:flex; justify-content:flex-start'>
        <div style='background:#2b313e; color:white;
                    padding:10px; border-radius:12px;
                    max-width:55%; margin:5px'>
            {a}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if sources:
        with st.expander("📄 Sources"):
            for s in sources:
                st.write(f"{s.get('file')} (Page {s.get('page')})")