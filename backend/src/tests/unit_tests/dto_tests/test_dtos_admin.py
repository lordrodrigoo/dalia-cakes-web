# pylint: disable=redefined-outer-name
from uuid import uuid4
from datetime import datetime
import pytest
from pydantic import ValidationError
from backend.src.dto.request.admin_request import AdminRequest
from backend.src.dto.request.login_request import LoginRequest
from backend.src.dto.request.refresh_token_request import RefreshTokenRequest
from backend.src.dto.request.role_request import RoleUpdateRequest
from backend.src.dto.response.admin_response import AdminResponse
from backend.src.domain.models.admin import AdminRole


# ──────────────────────────────────────────────
# fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def valid_user_data():
    return {
        "first_name": "Ana",
        "last_name": "Silva",
        "email": "ana.silva@example.com",
        "username": "ana.silva",
        "password": "Senha@123",
    }


# ──────────────────────────────────────────────
# AdminRequest — campo válido
# ──────────────────────────────────────────────

def test_valid_user_request(valid_user_data):
    req = AdminRequest(**valid_user_data)
    assert req.first_name == valid_user_data["first_name"]
    assert req.last_name == valid_user_data["last_name"]
    assert req.email == valid_user_data["email"]
    assert req.username == valid_user_data["username"]
    assert req.password == valid_user_data["password"]
    assert req.role == AdminRole.ADMIN  # default


def test_user_request_role_default(valid_user_data):
    req = AdminRequest(**valid_user_data)
    assert req.role == AdminRole.ADMIN


def test_user_request_role_owner(valid_user_data):
    req = AdminRequest(**valid_user_data, role=AdminRole.OWNER)
    assert req.role == AdminRole.OWNER


# ──────────────────────────────────────────────
# AdminRequest — validações de campo
# ──────────────────────────────────────────────

@pytest.mark.parametrize("field,value,expected_msg", [
    ("first_name", "Ab", "String should have at least 3 characters"),
    ("first_name", "A" * 26, "String should have at most 25 characters"),
    ("first_name", "John123", "must contain only letters."),
    ("last_name", "Si", "String should have at least 3 characters"),
    ("last_name", "S" * 26, "String should have at most 25 characters"),
    ("last_name", "Silva2", "must contain only letters."),
    ("email", "invalid-email", "value is not a valid email address"),
    ("username", "ab", "String should have at least 3 characters"),
    ("username", "a" * 26, "String should have at most 25 characters"),
    ("username", "john@@", "username must contain only letters, numbers, dots or underscores."),
    ("password", "short", "String should have at least 8 characters"),
    ("password", "weakpassword", "password must contain at least one uppercase"),
])
def test_user_request_field_validations(valid_user_data, field, value, expected_msg):
    data = valid_user_data.copy()
    data[field] = value

    with pytest.raises(ValidationError) as exc_info:
        AdminRequest(**data)

    assert expected_msg in str(exc_info.value)


# ──────────────────────────────────────────────
# LoginRequest
# ──────────────────────────────────────────────

def test_valid_login_request():
    req = LoginRequest(username="ana.silva", password="Senha@123")
    assert req.username == "ana.silva"
    assert req.password == "Senha@123"


@pytest.mark.parametrize("field,value,expected_msg", [
    ("username", "ab", "String should have at least 3 characters"),
    ("username", "user!@#", "username must contain only letters, numbers, dots or underscores."),
    ("password", "abc", "String should have at least 8 characters"),
    ("password", "weakpassword", "password must contain at least one uppercase"),
    ("password", "Password1234", "password must contain at least one uppercase"),
])
def test_login_request_field_validations(field, value, expected_msg):
    data = {"username": "ana.silva", "password": "Senha@123"}
    data[field] = value

    with pytest.raises(ValidationError) as exc_info:
        LoginRequest(**data)

    assert expected_msg in str(exc_info.value)


# ──────────────────────────────────────────────
# RefreshTokenRequest
# ──────────────────────────────────────────────

def test_valid_refresh_token_request():
    req = RefreshTokenRequest(refresh_token="a" * 10)
    assert req.refresh_token == "a" * 10


def test_refresh_token_too_short():
    with pytest.raises(ValidationError):
        RefreshTokenRequest(refresh_token="short")


# ──────────────────────────────────────────────
# RoleUpdateRequest
# ──────────────────────────────────────────────

def test_valid_role_update_request():
    req = RoleUpdateRequest(role=AdminRole.ADMIN)
    assert req.role == AdminRole.ADMIN


def test_role_update_invalid_value():
    with pytest.raises(ValidationError):
        RoleUpdateRequest(role="superuser")


# ──────────────────────────────────────────────
# AdminResponse
# ──────────────────────────────────────────────

def test_valid_user_response():
    now = datetime.now()
    resp = AdminResponse(
        id=uuid4(),
        first_name="Ana",
        last_name="Silva",
        email="ana.silva@example.com",
        username="ana.silva",
        role=AdminRole.ADMIN,
        created_at=now,
        updated_at=now,
    )
    assert resp.first_name == "Ana"
    assert resp.role == AdminRole.ADMIN


def test_user_response_missing_required_field():
    with pytest.raises(ValidationError):
        AdminResponse(
            first_name="Ana",
            last_name="Silva",
            email="ana.silva@example.com",
            username="ana.silva",
            role=AdminRole.ADMIN,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            # id ausente
        )
