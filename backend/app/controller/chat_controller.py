from app.models import ChatRequest, ChatResponse
from app.service.chat_service import answer_question


def handle_chat(request: ChatRequest) -> ChatResponse:
    return answer_question(request.question)
