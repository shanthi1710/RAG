import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings

EMBEDDING_MODEL = "models/gemini-embedding-001"


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )
