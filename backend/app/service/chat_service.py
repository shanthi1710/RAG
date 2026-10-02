from fastapi import HTTPException

from app.models import ChatResponse, RetrievedChunk
from app.rag.llm import generate_answer
from app.rag.vectorstore import search_similar_chunks

TOP_K = 3


def _build_context(retrieved_chunks: list[RetrievedChunk]) -> str:
    parts = [
        f"[Source: {chunk.filename}, page {chunk.page}]\n{chunk.content}"
        for chunk in retrieved_chunks
    ]
    return "\n\n".join(parts)


def answer_question(question: str) -> ChatResponse:
    # Question -> Embedding -> ChromaDB -> Relevant Chunks
    results = search_similar_chunks(question, k=TOP_K)

    retrieved_chunks = [
        RetrievedChunk(
            content=doc.page_content,
            filename=doc.metadata.get("filename", "unknown"),
            page=doc.metadata.get("page", -1),
            score=score,
        )
        for doc, score in results
    ]

    # Relevant Chunks -> Prompt + Context
    context = _build_context(retrieved_chunks)

    # Prompt + Context -> LLM -> Answer
    try:
        answer = generate_answer(question, context)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {exc}")

    return ChatResponse(question=question, answer=answer, retrieved_chunks=retrieved_chunks)
