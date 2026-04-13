from fastapi import APIRouter, Depends
from backend.src.dto.request.chatbot_request import ChatbotRequest
from backend.src.dto.response.chatbot_response import ChatbotResponse
from backend.src.usecases.chatbot_usecases import ChatbotUsecase
from backend.src.api.dependencies import get_chatbot_usecase

router = APIRouter(tags=["Chatbot"])


@router.post("/chatbot/message", response_model=ChatbotResponse, status_code=200)
def send_message(
    request: ChatbotRequest,
    chatbot_usecase: ChatbotUsecase = Depends(get_chatbot_usecase),
):
    return chatbot_usecase.chat(message=request.message, session_id=request.session_id)
