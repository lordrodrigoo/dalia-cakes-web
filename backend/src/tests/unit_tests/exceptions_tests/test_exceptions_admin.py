# pylint: disable=redefined-outer-name
from uuid import UUID
import pytest
from fastapi import status
from backend.src.tests.helpers import _call_handler
from backend.src.exceptions.exception_handlers_admin import (
    EmailAlreadyExistsException,
    AdminNotFoundException,
    UsernameAlreadyExistsException,
    AdminPermissionDeniedException,
    email_exception_handler,
    admin_not_found_exception_handler,
    username_exception_handler,
    admin_permission_denied_exception_handler,
)


# ──────────────────────────────────────────────
# EmailAlreadyExistsException
# ──────────────────────────────────────────────

def test_email_already_exists_attributes():
    exc = EmailAlreadyExistsException("test@email.com")
    assert exc.email == "test@email.com"
    assert "test@email.com" in exc.message


@pytest.mark.asyncio
async def test_email_already_exists_handler_returns_409():
    exc = EmailAlreadyExistsException("test@email.com")
    response = await _call_handler(email_exception_handler, exc)
    assert response.status_code == status.HTTP_409_CONFLICT


# ──────────────────────────────────────────────
# AdminNotFoundException
# ──────────────────────────────────────────────

def test_user_not_found_by_id():
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    exc = AdminNotFoundException(user_id=user_id)
    assert exc.user_id == user_id
    assert str(user_id) in exc.message


def test_user_not_found_by_email():
    exc = AdminNotFoundException(email="notfound@email.com")
    assert exc.email == "notfound@email.com"
    assert "notfound@email.com" in exc.message


@pytest.mark.asyncio
async def test_user_not_found_handler_returns_404():
    exc = AdminNotFoundException(user_id=UUID("00000000-0000-0000-0000-000000000001"))
    response = await _call_handler(admin_not_found_exception_handler, exc)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ──────────────────────────────────────────────
# UsernameAlreadyExistsException
# ──────────────────────────────────────────────

def test_username_already_exists_attributes():
    exc = UsernameAlreadyExistsException("ana.silva")
    assert exc.username == "ana.silva"
    assert "ana.silva" in exc.message


@pytest.mark.asyncio
async def test_username_already_exists_handler_returns_409():
    exc = UsernameAlreadyExistsException("ana.silva")
    response = await _call_handler(username_exception_handler, exc)
    assert response.status_code == status.HTTP_409_CONFLICT


# ──────────────────────────────────────────────
# AdminPermissionDeniedException
# ──────────────────────────────────────────────

def test_user_permission_denied_message():
    exc = AdminPermissionDeniedException()
    assert "permission" in exc.message.lower()


@pytest.mark.asyncio
async def test_user_permission_denied_handler_returns_403():
    exc = AdminPermissionDeniedException()
    response = await _call_handler(admin_permission_denied_exception_handler, exc)
    assert response.status_code == status.HTTP_403_FORBIDDEN
