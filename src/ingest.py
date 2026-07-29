from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

try:
    from .config import PDF_PATH
except ImportError:
    from config import PDF_PATH


def load_and_split_pdf(pdf_path=PDF_PATH, chunk_size=500, chunk_overlap=100):
    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return text_splitter.split_documents(documents)


def create_embeddings(chunks, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    texts = [chunk.page_content for chunk in chunks]
    return model.encode(texts)


if __name__ == "__main__":
    chunks = load_and_split_pdf(PDF_PATH)
    print(f"Created {len(chunks)} chunks")

    embeddings = create_embeddings(chunks)
    print(f"Embedding shape: {embeddings.shape}")

    if len(embeddings) > 0:
        print("\nFirst embedding (first 10 values):")
        print(embeddings[0][:10])
