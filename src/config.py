from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"

PDF_PATH = DATA_DIR / "sample.pdf"
FAISS_INDEX = VECTOR_STORE_DIR / "faiss_index.bin"
CHUNKS_FILE = VECTOR_STORE_DIR / "chunks.pkl"