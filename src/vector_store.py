import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

try:
    from .config import CHUNKS_FILE, FAISS_INDEX, PDF_PATH, VECTOR_STORE_DIR
    from .ingest import load_and_split_pdf
except ImportError:
    from config import CHUNKS_FILE, FAISS_INDEX, PDF_PATH, VECTOR_STORE_DIR
    from ingest import load_and_split_pdf


def create_vector_store(pdf_path=PDF_PATH):
    chunks = load_and_split_pdf(pdf_path)
    print(f"Created {len(chunks)} chunks")

    if not chunks:
        raise ValueError("No text chunks were created from the PDF.")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [chunk.page_content for chunk in chunks]
    embeddings = model.encode(texts)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    VECTOR_STORE_DIR.mkdir(exist_ok=True)
    faiss.write_index(index, str(FAISS_INDEX))

    with open(CHUNKS_FILE, "wb") as f:
        pickle.dump(chunks, f)

    print(f"Total vectors stored: {index.ntotal}")
    print("FAISS index saved!")
    print("Chunks saved!")

    return index, chunks


if __name__ == "__main__":
    create_vector_store(PDF_PATH)
