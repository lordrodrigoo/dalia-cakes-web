# pylint: disable=unused-argument
from fastapi import Request, status
from fastapi.responses import JSONResponse


class ChatbotUnavailableException(Exception):
    def __init__(self):
        self.message = "O serviço de chatbot está temporariamente indisponível. Tente novamente em breve."
        super().__init__(self.message)


async def chatbot_unavailable_exception_handler(request: Request, exc: ChatbotUnavailableException):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"message": exc.message}
    )
