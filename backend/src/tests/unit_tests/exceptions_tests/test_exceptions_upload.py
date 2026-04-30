# pylint: disable=redefined-outer-name
import json
import pytest
from fastapi import status
from backend.src.tests.helpers import _call_handler
from backend.src.exceptions.exception_handlers_upload import (
    ImageUploadException,
    image_upload_exception_handler,
    InvalidUploadFolderException,
    invalid_upload_folder_exception_handler,
    InvalidImageTypeException,
    invalid_image_type_exception_handler,
)


# ──────────────────────────────────────────────
# ImageUploadException
# ──────────────────────────────────────────────

def test_image_upload_exception_default_message():
    exc = ImageUploadException()
    assert exc.message
    assert str(exc) == exc.message


def test_image_upload_exception_custom_message():
    exc = ImageUploadException(message="Custom error")
    assert exc.message == "Custom error"


@pytest.mark.asyncio
async def test_image_upload_handler_returns_503():
    exc = ImageUploadException()
    response = await _call_handler(image_upload_exception_handler, exc)
    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


@pytest.mark.asyncio
async def test_image_upload_handler_body_contains_message():
    exc = ImageUploadException()
    response = await _call_handler(image_upload_exception_handler, exc)
    body = json.loads(response.body)
    assert "detail" in body
    assert body["detail"] == exc.message


# ──────────────────────────────────────────────
# InvalidUploadFolderException
# ──────────────────────────────────────────────

def test_invalid_upload_folder_exception_default_message():
    exc = InvalidUploadFolderException()
    assert exc.message
    assert str(exc) == exc.message


def test_invalid_upload_folder_exception_custom_message():
    exc = InvalidUploadFolderException(message="Folder X not allowed")
    assert exc.message == "Folder X not allowed"


@pytest.mark.asyncio
async def test_invalid_upload_folder_handler_returns_400():
    exc = InvalidUploadFolderException()
    response = await _call_handler(invalid_upload_folder_exception_handler, exc)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_invalid_upload_folder_handler_body_contains_message():
    exc = InvalidUploadFolderException()
    response = await _call_handler(invalid_upload_folder_exception_handler, exc)
    body = json.loads(response.body)
    assert "detail" in body
    assert body["detail"] == exc.message


# ──────────────────────────────────────────────
# InvalidImageTypeException
# ──────────────────────────────────────────────

def test_invalid_image_type_exception_default_message():
    exc = InvalidImageTypeException()
    assert exc.message
    assert str(exc) == exc.message


def test_invalid_image_type_exception_custom_message():
    exc = InvalidImageTypeException(message="Only PNG allowed")
    assert exc.message == "Only PNG allowed"


@pytest.mark.asyncio
async def test_invalid_image_type_handler_returns_400():
    exc = InvalidImageTypeException()
    response = await _call_handler(invalid_image_type_exception_handler, exc)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_invalid_image_type_handler_body_contains_message():
    exc = InvalidImageTypeException()
    response = await _call_handler(invalid_image_type_exception_handler, exc)
    body = json.loads(response.body)
    assert "detail" in body
    assert body["detail"] == exc.message
