try:
    from .retrieval import load_vector_store, retrieve
except ImportError:
    from retrieval import load_vector_store, retrieve


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
