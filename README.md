# 📄 RAG PDF Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built using Python, FAISS, Sentence Transformers, Google Gemini, and Streamlit.

## Features

- Upload PDF documents
- Semantic search using FAISS
- Google Gemini integration
- Interactive Streamlit UI
- Local embeddings with Sentence Transformers

## Tech Stack

- Python
- Streamlit
- FAISS
- Sentence Transformers
- Google Gemini API
- LangChain (PDF Loader)

## Project Structure

```
rag-chatbot/
│
├── app.py
├── data/
├── src/
├── vector_store/
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone <repo-url>
cd rag-chatbot

python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```
GOOGLE_API_KEY=YOUR_API_KEY
```

Run:

```bash
streamlit run app.py
```

## Architecture

```
PDF
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS
 ↓
Retrieve
 ↓
Gemini
 ↓
Answer
```