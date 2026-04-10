# pylint: disable=redefined-outer-name
from uuid import UUID
import pytest
from fastapi import status
from backend.src.tests.helpers import _call_handler
from backend.src.exceptions.exception_handlers_product import (
    ProductNotFoundException,
    ProductCategoryNotFoundException,
    product_not_found_exception_handler,
    product_category_not_found_exception_handler,
)


# ──────────────────────────────────────────────
# ProductNotFoundException
# ──────────────────────────────────────────────

def test_product_not_found_attributes():
    product_id = UUID("00000000-0000-0000-0000-000000000001")
    exc = ProductNotFoundException(product_id=product_id)
    assert exc.product_id == product_id
    assert str(product_id) in exc.message


@pytest.mark.asyncio
async def test_product_not_found_handler_returns_404():
    product_id = UUID("00000000-0000-0000-0000-000000000001")
    exc = ProductNotFoundException(product_id=product_id)
    response = await _call_handler(product_not_found_exception_handler, exc)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# ──────────────────────────────────────────────
# ProductCategoryNotFoundException
# ──────────────────────────────────────────────

def test_product_category_not_found_attributes():
    category_id = UUID("00000000-0000-0000-0000-000000000002")
    exc = ProductCategoryNotFoundException(category_id=category_id)
    assert exc.category_id == category_id
    assert str(category_id) in exc.message


@pytest.mark.asyncio
async def test_product_category_not_found_handler_returns_404():
    category_id = UUID("00000000-0000-0000-0000-000000000002")
    exc = ProductCategoryNotFoundException(category_id=category_id)
    response = await _call_handler(product_category_not_found_exception_handler, exc)
    assert response.status_code == status.HTTP_404_NOT_FOUND
