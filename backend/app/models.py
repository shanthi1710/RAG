from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    num_pages: int
    num_chunks: int
    num_chunks_stored: int
    saved_path: str


class ChatRequest(BaseModel):
    question: str


class RetrievedChunk(BaseModel):
    content: str
    filename: str
    page: int
    score: float


class ChatResponse(BaseModel):
    question: str
    answer: str
    retrieved_chunks: list[RetrievedChunk]
