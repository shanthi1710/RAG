import os

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import BASE_DIR
from app.rag.embeddings import get_embedding_model

PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "documents"

_vectorstore: Chroma | None = None


def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=get_embedding_model(),
            persist_directory=PERSIST_DIR,
        )
    return _vectorstore


def add_documents(documents: list[Document]) -> list[str]:
    return get_vectorstore().add_documents(documents)


def search_similar_chunks(query: str, k: int = 3) -> list[tuple[Document, float]]:
    return get_vectorstore().similarity_search_with_score(query, k=k)
