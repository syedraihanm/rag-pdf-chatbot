import os

from dotenv import load_dotenv
from google import genai

try:
    from .retrieval import retrieve
except ImportError:
    from retrieval import retrieve


def answer_question(question, k=3):
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    chunks = retrieve(question, k=k)
    context = "\n\n".join(chunk.page_content for chunk in chunks)

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the context below.

If the answer is not found in the context, reply:
"I couldn't find that information in the document."

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )

    return response.text


if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:\n")
        print(answer)
