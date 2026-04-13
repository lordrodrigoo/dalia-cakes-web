# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock, patch
import pytest
import httpx
from backend.src.infra.gemini.gemini_client import GeminiClient


@pytest.fixture
def client():
    return GeminiClient(api_key="fake-api-key", model="gemini-2.0-flash")


# ──────────────────────────────────────────────
# send_message — sucesso
# ──────────────────────────────────────────────

def test_send_message_returns_reply(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "candidates": [
            {"content": {"parts": [{"text": "Estamos abertos das 8h às 18h!"}]}}
        ]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("backend.src.infra.gemini.gemini_client.httpx.post", return_value=mock_response):
        result = client.send_message(
            message="Qual o horário?",
            history=[],
            system_prompt="Você é um assistente.",
        )

    assert result == "Estamos abertos das 8h às 18h!"


def test_send_message_passes_history(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Ok!"}]}}]
    }
    mock_response.raise_for_status = MagicMock()

    history = [
        {"role": "user", "parts": [{"text": "Oi"}]},
        {"role": "model", "parts": [{"text": "Olá!"}]},
    ]

    with patch("backend.src.infra.gemini.gemini_client.httpx.post", return_value=mock_response) as mock_post:
        client.send_message(message="Qual o preço?", history=history, system_prompt="...")

    called_payload = mock_post.call_args[1]["json"]
    assert len(called_payload["contents"]) == 3  # 2 history + 1 current
    assert called_payload["contents"][2]["role"] == "user"
    assert called_payload["contents"][2]["parts"][0]["text"] == "Qual o preço?"


def test_send_message_sends_system_prompt(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Ok"}]}}]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("backend.src.infra.gemini.gemini_client.httpx.post", return_value=mock_response) as mock_post:
        client.send_message(message="Oi", history=[], system_prompt="Meu prompt especial")

    called_payload = mock_post.call_args[1]["json"]
    assert called_payload["system_instruction"]["parts"][0]["text"] == "Meu prompt especial"


def test_send_message_uses_api_key_in_params(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Ok"}]}}]
    }
    mock_response.raise_for_status = MagicMock()

    with patch("backend.src.infra.gemini.gemini_client.httpx.post", return_value=mock_response) as mock_post:
        client.send_message(message="Oi", history=[], system_prompt="...")

    called_params = mock_post.call_args[1]["params"]
    assert called_params["key"] == "fake-api-key"


# ──────────────────────────────────────────────
# send_message — erros
# ──────────────────────────────────────────────

def test_send_message_raises_on_http_error(client):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "403 Forbidden", request=MagicMock(), response=MagicMock()
    )

    with patch("backend.src.infra.gemini.gemini_client.httpx.post", return_value=mock_response):
        with pytest.raises(httpx.HTTPStatusError):
            client.send_message(message="Oi", history=[], system_prompt="...")


def test_send_message_raises_on_network_error(client):
    with patch(
        "backend.src.infra.gemini.gemini_client.httpx.post",
        side_effect=httpx.ConnectError("connection refused"),
    ):
        with pytest.raises(httpx.ConnectError):
            client.send_message(message="Oi", history=[], system_prompt="...")
