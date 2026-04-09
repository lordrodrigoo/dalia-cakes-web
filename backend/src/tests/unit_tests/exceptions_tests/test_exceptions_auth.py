# pylint: disable=redefined-outer-name
import pytest
from fastapi import status
from backend.src.tests.helpers import _call_handler
from backend.src.exceptions.exception_handlers_auth import (
    TokenExpiredException,
    TokenInvalidException,
    InvalidCredentialsException,
    token_expired_exception_handler,
    token_invalid_exception_handler,
    invalid_credentials_exception_handler,
)


# ──────────────────────────────────────────────
# TokenExpiredException
# ──────────────────────────────────────────────

def test_token_expired_default_message():
    exc = TokenExpiredException()
    assert "expired" in exc.message.lower()


def test_token_expired_custom_message():
    exc = TokenExpiredException("custom expired message")
    assert exc.message == "custom expired message"


@pytest.mark.asyncio
async def test_token_expired_handler_returns_401():
    exc = TokenExpiredException()
    response = await _call_handler(token_expired_exception_handler, exc)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ──────────────────────────────────────────────
# TokenInvalidException
# ──────────────────────────────────────────────

def test_token_invalid_default_message():
    exc = TokenInvalidException()
    assert "invalid" in exc.message.lower()


def test_token_invalid_custom_message():
    exc = TokenInvalidException("bad token")
    assert exc.message == "bad token"


@pytest.mark.asyncio
async def test_token_invalid_handler_returns_401():
    exc = TokenInvalidException()
    response = await _call_handler(token_invalid_exception_handler, exc)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ──────────────────────────────────────────────
# InvalidCredentialsException
# ──────────────────────────────────────────────

def test_invalid_credentials_default_message():
    exc = InvalidCredentialsException()
    assert "invalid" in exc.message.lower()


def test_invalid_credentials_custom_message():
    exc = InvalidCredentialsException("wrong password")
    assert exc.message == "wrong password"


@pytest.mark.asyncio
async def test_invalid_credentials_handler_returns_401():
    exc = InvalidCredentialsException()
    response = await _call_handler(invalid_credentials_exception_handler, exc)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
