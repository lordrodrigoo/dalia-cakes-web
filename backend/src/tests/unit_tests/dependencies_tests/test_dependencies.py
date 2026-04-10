# pylint: disable=redefined-outer-name
from uuid import uuid4
from datetime import datetime
from unittest.mock import MagicMock, patch
import pytest
from backend.src.domain.models.admin import AdminRole
from backend.src.dto.response.admin_response import AdminResponse
from backend.src.dto.response.token_response import TokenPayload
from backend.src.usecases.admin_usecases import AdminUsecase
from backend.src.usecases.auth_usecases import AuthUsecase
from backend.src.usecases.category_usecases import CategoryUsecase
from backend.src.usecases.product_usecases import ProductUsecase
from backend.src.api.dependencies import (
    get_db,
    get_admin_usecase,
    get_auth_usecase,
    get_current_user,
    get_category_usecase,
    get_product_usecase,
)


# ──────────────────────────────────────────────
# get_db
# ──────────────────────────────────────────────

def test_get_db_yields_db_handler():
    mock_db = MagicMock()
    mock_db.__enter__ = MagicMock(return_value=mock_db)
    mock_db.__exit__ = MagicMock(return_value=False)

    with patch("backend.src.api.dependencies.DBConnectionHandler", return_value=mock_db):
        gen = get_db()
        db = next(gen)
        assert db is mock_db
        try:
            next(gen)
        except StopIteration:
            pass


# ──────────────────────────────────────────────
# get_admin_usecase
# ──────────────────────────────────────────────

def test_get_admin_usecase_returns_admin_usecase():
    mock_db = MagicMock()
    result = get_admin_usecase(db=mock_db)
    assert isinstance(result, AdminUsecase)


# ──────────────────────────────────────────────
# get_auth_usecase
# ──────────────────────────────────────────────

def test_get_auth_usecase_returns_auth_usecase():
    mock_db = MagicMock()
    result = get_auth_usecase(db=mock_db)
    assert isinstance(result, AuthUsecase)


# ──────────────────────────────────────────────
# get_category_usecase
# ──────────────────────────────────────────────

def test_get_category_usecase_returns_category_usecase():
    mock_db = MagicMock()
    result = get_category_usecase(db=mock_db)
    assert isinstance(result, CategoryUsecase)


# ──────────────────────────────────────────────
# get_product_usecase
# ──────────────────────────────────────────────

def test_get_product_usecase_returns_product_usecase():
    mock_db = MagicMock()
    result = get_product_usecase(db=mock_db)
    assert isinstance(result, ProductUsecase)


# ──────────────────────────────────────────────
# get_current_user
# ──────────────────────────────────────────────

@pytest.fixture
def fake_admin_response():
    return AdminResponse(
        id=uuid4(),
        first_name="Dalia",
        last_name="Silva",
        email="dalia@example.com",
        username="dalia.silva",
        role=AdminRole.OWNER,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def test_get_current_user_returns_admin_response(fake_admin_response):
    credentials = MagicMock()
    credentials.credentials = "valid.jwt.token"

    token_payload = TokenPayload(
        sub=fake_admin_response.id,
        role=fake_admin_response.role.value,
        exp=9999999999,
    )

    admin_usecase = MagicMock()
    admin_usecase.get_admin_by_id.return_value = fake_admin_response

    with patch("backend.src.api.dependencies.verify_token", return_value=token_payload):
        result = get_current_user(credentials=credentials, admin_usecase=admin_usecase)

    assert result is fake_admin_response
    admin_usecase.get_admin_by_id.assert_called_once_with(token_payload.sub)
