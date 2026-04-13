# pylint: disable=redefined-outer-name
import json
from uuid import UUID
import pytest
from fastapi import status
from backend.src.tests.helpers import _call_handler
from backend.src.exceptions.exception_handlers_instagram import (
    InstagramPostNotFoundException,
    DecoratedCakeNotFoundException,
    instagram_post_not_found_exception_handler,
    decorated_cake_not_found_exception_handler,
)


# ──────────────────────────────────────────────
# InstagramPostNotFoundException
# ──────────────────────────────────────────────

def test_instagram_post_not_found_attributes():
    post_id = UUID("00000000-0000-0000-0000-000000000001")
    exc = InstagramPostNotFoundException(post_id=post_id)
    assert exc.post_id == post_id
    assert str(post_id) in exc.message


def test_instagram_post_not_found_message_format():
    post_id = UUID("00000000-0000-0000-0000-000000000002")
    exc = InstagramPostNotFoundException(post_id=post_id)
    assert "Instagram post" in exc.message
    assert "not found" in exc.message


@pytest.mark.asyncio
async def test_instagram_post_not_found_handler_returns_404():
    post_id = UUID("00000000-0000-0000-0000-000000000001")
    exc = InstagramPostNotFoundException(post_id=post_id)
    response = await _call_handler(instagram_post_not_found_exception_handler, exc)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_instagram_post_not_found_handler_response_body():
    post_id = UUID("00000000-0000-0000-0000-000000000001")
    exc = InstagramPostNotFoundException(post_id=post_id)
    response = await _call_handler(instagram_post_not_found_exception_handler, exc)
    body = json.loads(response.body)
    assert "message" in body
    assert str(post_id) in body["message"]


# ──────────────────────────────────────────────
# DecoratedCakeNotFoundException
# ──────────────────────────────────────────────

def test_decorated_cake_not_found_attributes():
    subcategory_id = UUID("00000000-0000-0000-0000-000000000003")
    exc = DecoratedCakeNotFoundException(subcategory_id=subcategory_id)
    assert exc.subcategory_id == subcategory_id
    assert str(subcategory_id) in exc.message


def test_decorated_cake_not_found_message_format():
    subcategory_id = UUID("00000000-0000-0000-0000-000000000004")
    exc = DecoratedCakeNotFoundException(subcategory_id=subcategory_id)
    assert "Decorated cake" in exc.message
    assert "not found" in exc.message


@pytest.mark.asyncio
async def test_decorated_cake_not_found_handler_returns_404():
    subcategory_id = UUID("00000000-0000-0000-0000-000000000003")
    exc = DecoratedCakeNotFoundException(subcategory_id=subcategory_id)
    response = await _call_handler(decorated_cake_not_found_exception_handler, exc)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_decorated_cake_not_found_handler_response_body():
    subcategory_id = UUID("00000000-0000-0000-0000-000000000003")
    exc = DecoratedCakeNotFoundException(subcategory_id=subcategory_id)
    response = await _call_handler(decorated_cake_not_found_exception_handler, exc)
    body = json.loads(response.body)
    assert "message" in body
    assert str(subcategory_id) in body["message"]
