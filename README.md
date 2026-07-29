# 📄 RAG PDF Chatbot

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)

An end-to-end **Retrieval-Augmented Generation (RAG)** system designed to extract, index, and query unstructured information from PDF documents. By combining **local open-source embeddings** with **Google Gemini**, the application delivers context-grounded answers without transferring sensitive document vectors to third-party embedding providers.

---

## 🏗️ System Architecture

```
                                [ PDF Document ]
                                       │
                                       ▼
                             [ PyPDF Document Loader ]
                                       │
                                       ▼
                          [ Recursive Text Splitter ]
                             (1000 chars / 200 overlap)
                                       │
                                       ▼
                       [ Sentence-Transformers Embeddings ]
                           (all-MiniLM-L6-v2 / Local)
                                       │
                                       ▼
                       [ FAISS In-Memory Vector Store ]
                                       │
                                       ├─────────────────────────────┐
                                       ▼                             ▼
  [ User Query ] ──► [ Similarity Search (k=4) ]          [ Persisted Index ]
                                       │
                                       ▼
                          [ Relevant Context Chunks ]
                                       │
                                       ▼
                       [ Google Gemini LLM Prompt ]
                                       │
                                       ▼
                             [ Grounded Response ]
```

---

## ✨ Key Features

- **🔒 Local Embeddings:** Utilizes `sentence-transformers/all-MiniLM-L6-v2` locally for efficient, zero-cost vector computations.
- **⚡ Fast Vector Retrieval:** FAISS vector store enables ultra-low-latency similarity indexing and context retrieval.
- **🤖 Powered by Google Gemini:** High-precision text synthesis using Google's generative models with custom contextual prompts.
- **💬 Interactive Chat Interface:** Native Streamlit chat primitives with persistent conversational session state.
- **📁 Multi-Document Support:** Load and query across multiple PDF uploads within a single session.

---

## 📂 Project Structure

```text
rag-chatbot/
├── data/                  # Source PDF files directory
├── vector_store/          # Saved local FAISS vector indices
├── src/
│   ├── __init__.py
│   ├── document_loader.py # PDF parsing and chunking logic
│   ├── vector_db.py       # FAISS indexing and retrieval wrappers
│   └── rag_chain.py       # Gemini prompt formatting and pipeline execution
├── app.py                 # Streamlit UI dashboard
├── requirements.txt       # Project dependencies
├── .env.example           # Environment variables template
└── README.md              # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.9+ installed
- Google Gemini API Key ([Get an API Key here](https://aistudio.google.com/))

### 2. Clone and Setup

```bash
# Clone the repository
git clone [https://github.com/your-username/rag-pdf-chatbot.git](https://github.com/your-username/rag-pdf-chatbot.git)
cd rag-pdf-chatbot

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the template environment file and insert your API key:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```

---

## 💻 Usage

Run the Streamlit application interface:

```bash
streamlit run app.py
```

1. Navigate to `http://localhost:8501` in your web browser.
2. Upload your PDF file(s) using the sidebar file uploader.
3. Click **Process Documents** to generate local embeddings and index them into FAISS.
4. Type natural-language questions in the chat input field to interact with your documents!

---

## ⚙️ Configuration & Hyperparameters

| Parameter | Default Value | Description |
| :--- | :--- | :--- |
| **Chunk Size** | `1000` | Target character count per document chunk |
| **Chunk Overlap** | `200` | Overlapping characters between adjacent chunks to maintain context |
| **Embedding Model** | `all-MiniLM-L6-v2` | Lightweight Hugging Face transformer model |
| **Search Type** | Similarity ($k=4$) | Retrieves top-4 matching chunks from the FAISS database |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to open a Pull Request or create an Issue to discuss potential features and bug fixes.

---

