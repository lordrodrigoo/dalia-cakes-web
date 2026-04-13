# pylint: disable=redefined-outer-name
# pylint: disable=protected-access
from decimal import Decimal
from datetime import datetime
from uuid import uuid4
import pytest
from backend.src.domain.models.product import Product
from backend.src.domain.models.category import Category
from backend.src.exceptions.exception_handlers_chatbot import ChatbotUnavailableException
from backend.src.usecases import chatbot_usecases as chatbot_module


# ──────────────────────────────────────────────
# chat — nova sessão
# ──────────────────────────────────────────────

def test_chat_creates_new_session(chatbot_usecase, gemini_client_mock, product_repository_mock, category_repository_mock):
    product_repository_mock.get_all_products.return_value = []
    category_repository_mock.get_all_categories.return_value = []
    gemini_client_mock.send_message.return_value = "Olá! Como posso ajudar?"

    response = chatbot_usecase.chat(message="Oi", session_id=None)

    assert response.reply == "Olá! Como posso ajudar?"
    assert response.session_id is not None
    assert len(response.session_id) > 0


def test_chat_returns_session_id_provided(chatbot_usecase, gemini_client_mock, product_repository_mock, category_repository_mock):
    product_repository_mock.get_all_products.return_value = []
    category_repository_mock.get_all_categories.return_value = []
    gemini_client_mock.send_message.return_value = "Perfeito!"

    response = chatbot_usecase.chat(message="Qual o horário?", session_id="minha-sessao-123")

    assert response.session_id == "minha-sessao-123"


def test_chat_stores_history(chatbot_usecase, gemini_client_mock, product_repository_mock, category_repository_mock):
    product_repository_mock.get_all_products.return_value = []
    category_repository_mock.get_all_categories.return_value = []
    gemini_client_mock.send_message.return_value = "Resposta 1"

    chatbot_usecase.chat(message="Pergunta 1", session_id="sessao-hist")
    gemini_client_mock.send_message.return_value = "Resposta 2"
    chatbot_usecase.chat(message="Pergunta 2", session_id="sessao-hist")

    history = chatbot_module._chat_history.get("sessao-hist", [])
    assert len(history) == 4  # 2 user + 2 model


def test_chat_passes_history_to_gemini(chatbot_usecase, gemini_client_mock, product_repository_mock, category_repository_mock):
    product_repository_mock.get_all_products.return_value = []
    category_repository_mock.get_all_categories.return_value = []
    gemini_client_mock.send_message.return_value = "Ok"

    chatbot_usecase.chat(message="Primeira", session_id="sessao-pass")
    chatbot_usecase.chat(message="Segunda", session_id="sessao-pass")

    second_call_history = gemini_client_mock.send_message.call_args[1]["history"]
    assert len(second_call_history) == 2  # user + model da primeira pergunta


# ──────────────────────────────────────────────
# chat — trimming do histórico
# ──────────────────────────────────────────────

def test_chat_trims_history_when_exceeds_max(chatbot_usecase, gemini_client_mock, product_repository_mock, category_repository_mock):
    product_repository_mock.get_all_products.return_value = []
    category_repository_mock.get_all_categories.return_value = []
    gemini_client_mock.send_message.return_value = "resp"

    session_id = "sessao-trim"
    for i in range(15):
        chatbot_usecase.chat(message=f"msg {i}", session_id=session_id)

    history = chatbot_module._chat_history.get(session_id, [])
    # CHATBOT_MAX_HISTORY default = 10, so max_entries = 20
    assert len(history) <= 20


# ──────────────────────────────────────────────
# chat — Gemini falha
# ──────────────────────────────────────────────

def test_chat_raises_chatbot_unavailable_when_gemini_fails(chatbot_usecase, gemini_client_mock, product_repository_mock, category_repository_mock):
    product_repository_mock.get_all_products.return_value = []
    category_repository_mock.get_all_categories.return_value = []
    gemini_client_mock.send_message.side_effect = Exception("network error")

    with pytest.raises(ChatbotUnavailableException):
        chatbot_usecase.chat(message="Oi", session_id=None)


# ──────────────────────────────────────────────
# _build_system_prompt — conteúdo
# ──────────────────────────────────────────────

def test_system_prompt_includes_products(chatbot_usecase, product_repository_mock, category_repository_mock):
    product_repository_mock.get_all_products.return_value = [
        Product(
            id=uuid4(), name="Bolo de Chocolate", price=Decimal("55.00"),
            image_url=None, category_id=uuid4(),
            created_at=datetime.now(), updated_at=datetime.now(),
        )
    ]
    category_repository_mock.get_all_categories.return_value = []

    prompt = chatbot_usecase._build_system_prompt()  # pylint: disable=protected-access

    assert "Bolo de Chocolate" in prompt
    assert "55.00" in prompt


def test_system_prompt_includes_categories(chatbot_usecase, product_repository_mock, category_repository_mock):
    product_repository_mock.get_all_products.return_value = []
    category_repository_mock.get_all_categories.return_value = [
        Category(
            id=uuid4(), name="Bolos", slug="bolos", image_url=None,
            created_at=datetime.now(), updated_at=datetime.now(),
        )
    ]

    prompt = chatbot_usecase._build_system_prompt()

    assert "Bolos" in prompt


def test_system_prompt_empty_products_shows_fallback(chatbot_usecase, product_repository_mock, category_repository_mock):
    product_repository_mock.get_all_products.return_value = []
    category_repository_mock.get_all_categories.return_value = []

    prompt = chatbot_usecase._build_system_prompt()

    assert "WhatsApp" in prompt
