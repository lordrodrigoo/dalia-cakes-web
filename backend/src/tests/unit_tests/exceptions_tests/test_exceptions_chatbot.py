# pylint: disable=redefined-outer-name
import json
import pytest
from fastapi import status
from backend.src.tests.helpers import _call_handler
from backend.src.exceptions.exception_handlers_chatbot import (
    ChatbotUnavailableException,
    chatbot_unavailable_exception_handler,
)


# ──────────────────────────────────────────────
# ChatbotUnavailableException
# ──────────────────────────────────────────────

def test_chatbot_unavailable_exception_message():
    exc = ChatbotUnavailableException()
    assert "indisponível" in exc.message
    assert str(exc) == exc.message


@pytest.mark.asyncio
async def test_chatbot_unavailable_handler_returns_503():
    exc = ChatbotUnavailableException()
    response = await _call_handler(chatbot_unavailable_exception_handler, exc)
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


@pytest.mark.asyncio
async def test_chatbot_unavailable_handler_body_contains_message():
    exc = ChatbotUnavailableException()
    response = await _call_handler(chatbot_unavailable_exception_handler, exc)
    body = json.loads(response.body)
    assert "message" in body
    assert body["message"] == exc.message
