import tempfile

import streamlit as st

from src.chat import answer_question
from src.vector_store import create_vector_store

st.set_page_config(
    page_title="RAG PDF Chatbot",
    layout="wide",
)

st.title("RAG PDF Chatbot")

with st.sidebar:
    st.header("Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type="pdf",
    )

    if uploaded_file:
        file_bytes = uploaded_file.getvalue()
        file_key = (uploaded_file.name, uploaded_file.size)

        if st.session_state.get("indexed_file_key") != file_key:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file_bytes)
                pdf_path = tmp.name

            with st.spinner("Creating vector store..."):
                create_vector_store(pdf_path)

            st.session_state["indexed_file_key"] = file_key

        st.success("PDF indexed!")

if "indexed_file_key" not in st.session_state:
    st.info("Upload a PDF to start chatting with it.")

st.write("Ask questions about your PDF.")
question = st.text_input("Ask a question about the document")

if st.button("Ask") and question:
    if "indexed_file_key" not in st.session_state:
        st.warning("Please upload a PDF first.")
    else:
        with st.spinner("Thinking..."):
            answer = answer_question(question)

        st.write(answer)
