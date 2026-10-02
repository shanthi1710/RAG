import os

from langchain_google_genai import ChatGoogleGenerativeAI

CHAT_MODEL = "models/gemini-3.8-flash"


def get_chat_model() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=CHAT_MODEL,
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )


def generate_answer(question: str, context: str) -> str:
    prompt = (
        "Answer the question using only the context below.\n"
        "If the answer is not contained in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )

    model = get_chat_model()
    response = model.invoke(prompt)
    return response.text
