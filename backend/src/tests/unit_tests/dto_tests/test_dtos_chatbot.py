# pylint: disable=redefined-outer-name
import pytest
from pydantic import ValidationError as PydanticValidationError
from backend.src.dto.request.chatbot_request import ChatbotRequest
from backend.src.dto.response.chatbot_response import ChatbotResponse


# ──────────────────────────────────────────────
# ChatbotRequest
# ──────────────────────────────────────────────

def test_chatbot_request_valid():
    req = ChatbotRequest(message="Qual o horário de funcionamento?")
    assert req.message == "Qual o horário de funcionamento?"
    assert req.session_id is None


def test_chatbot_request_with_session_id():
    req = ChatbotRequest(message="Olá!", session_id="abc-123")
    assert req.session_id == "abc-123"


def test_chatbot_request_empty_message_raises():
    with pytest.raises(PydanticValidationError):
        ChatbotRequest(message="")


def test_chatbot_request_message_too_long_raises():
    with pytest.raises(PydanticValidationError):
        ChatbotRequest(message="x" * 1001)


def test_chatbot_request_max_length_ok():
    req = ChatbotRequest(message="x" * 1000)
    assert len(req.message) == 1000


# ──────────────────────────────────────────────
# ChatbotResponse
# ──────────────────────────────────────────────

def test_chatbot_response_valid():
    resp = ChatbotResponse(reply="Olá! Estamos abertos das 8h às 18h.", session_id="abc-123")
    assert resp.reply == "Olá! Estamos abertos das 8h às 18h."
    assert resp.session_id == "abc-123"
