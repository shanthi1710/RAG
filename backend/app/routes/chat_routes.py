from fastapi import APIRouter

from app.controller.chat_controller import handle_chat
from app.models import ChatRequest, ChatResponse

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return handle_chat(request)
