# pylint: disable=redefined-outer-name
from uuid import UUID
import pytest
from fastapi import status
from backend.src.tests.helpers import _call_handler
from backend.src.exceptions.exception_handlers_category import (
    CategoryNotFoundException,
    CategoryNameAlreadyExistsException,
    CategorySlugAlreadyExistsException,
    category_not_found_exception_handler,
    category_name_already_exists_exception_handler,
    category_slug_already_exists_exception_handler,
)


# ──────────────────────────────────────────────
# CategoryNotFoundException — por ID
# ──────────────────────────────────────────────

def test_category_not_found_by_id_attributes():
    category_id = UUID("00000000-0000-0000-0000-000000000001")
    exc = CategoryNotFoundException(category_id=category_id)
    assert str(category_id) in exc.message


@pytest.mark.asyncio
async def test_category_not_found_by_id_handler_returns_404():
    category_id = UUID("00000000-0000-0000-0000-000000000001")
    exc = CategoryNotFoundException(category_id=category_id)
    response = await _call_handler(category_not_found_exception_handler, exc)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ──────────────────────────────────────────────
# CategoryNotFoundException — por slug
# ──────────────────────────────────────────────

def test_category_not_found_by_slug_attributes():
    exc = CategoryNotFoundException(slug="bolos-decorados")
    assert "bolos-decorados" in exc.message


@pytest.mark.asyncio
async def test_category_not_found_by_slug_handler_returns_404():
    exc = CategoryNotFoundException(slug="bolos-decorados")
    response = await _call_handler(category_not_found_exception_handler, exc)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ──────────────────────────────────────────────
# CategoryNameAlreadyExistsException
# ──────────────────────────────────────────────

def test_category_name_already_exists_attributes():
    exc = CategoryNameAlreadyExistsException("Bolos Decorados")
    assert exc.name == "Bolos Decorados"
    assert "Bolos Decorados" in exc.message


@pytest.mark.asyncio
async def test_category_name_already_exists_handler_returns_409():
    exc = CategoryNameAlreadyExistsException("Bolos Decorados")
    response = await _call_handler(category_name_already_exists_exception_handler, exc)
    assert response.status_code == status.HTTP_409_CONFLICT


# ──────────────────────────────────────────────
# CategorySlugAlreadyExistsException
# ──────────────────────────────────────────────

def test_category_slug_already_exists_attributes():
    exc = CategorySlugAlreadyExistsException("bolos-decorados")
    assert exc.slug == "bolos-decorados"
    assert "bolos-decorados" in exc.message


@pytest.mark.asyncio
async def test_category_slug_already_exists_handler_returns_409():
    exc = CategorySlugAlreadyExistsException("bolos-decorados")
    response = await _call_handler(category_slug_already_exists_exception_handler, exc)
    assert response.status_code == status.HTTP_409_CONFLICT
