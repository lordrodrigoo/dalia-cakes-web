from pydantic import BaseModel


class ChatbotResponse(BaseModel):
    reply: str
    session_id: str
