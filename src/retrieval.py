import pickle

import faiss
from sentence_transformers import SentenceTransformer

try:
    from .config import CHUNKS_FILE, FAISS_INDEX
except ImportError:
    from config import CHUNKS_FILE, FAISS_INDEX


def load_vector_store(index_path=FAISS_INDEX, chunks_file=CHUNKS_FILE):
    index = faiss.read_index(str(index_path))

    with open(chunks_file, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


def retrieve(query, k=3):
    ##model = SentenceTransformer("all-MiniLM-L6-v2")
    model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=True
)
    index, chunks = load_vector_store()

    query_embedding = model.encode([query]).astype("float32")
    _, indices = index.search(query_embedding, min(k, len(chunks)))

    return [chunks[i] for i in indices[0] if i != -1]


if __name__ == "__main__":
    while True:
        query = input("\nAsk a question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        results = retrieve(query)

        print("\nTop relevant chunks:\n")

        for i, chunk in enumerate(results, start=1):
            print("=" * 60)
            print(f"Result {i}")
            print("=" * 60)
            print(chunk.page_content)
            print()
