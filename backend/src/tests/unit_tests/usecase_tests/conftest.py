# pylint: disable=redefined-outer-name
from uuid import uuid4
from datetime import datetime
from unittest.mock import MagicMock
import pytest
from backend.src.domain.models.admin import Admin, AdminRole
from backend.src.dto.response.admin_response import AdminResponse
from backend.src.usecases.admin_usecases import AdminUsecase
from backend.src.usecases.auth_usecases import AuthUsecase
from backend.src.config.security import hash_password


@pytest.fixture
def admin_repository_mock():
    return MagicMock()


@pytest.fixture
def usecase(admin_repository_mock):
    return AdminUsecase(admin_repository_mock)


@pytest.fixture
def owner_user():
    return AdminResponse(
        id=uuid4(),
        first_name="Dalia",
        last_name="Owner",
        email="dalia@example.com",
        username="dalia.owner",
        role=AdminRole.OWNER,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


# ── auth fixtures ──────────────────────────────

@pytest.fixture
def auth_repository_mock():
    return MagicMock()


@pytest.fixture
def auth_usecase(auth_repository_mock):
    return AuthUsecase(auth_repository_mock)


@pytest.fixture
def fake_auth_user():
    return Admin(
        id=uuid4(),
        first_name="Rodrigo",
        last_name="Souza",
        username="rodrigo.souza",
        email="rodrigo@example.com",
        password=hash_password("P@ssw0rd1"),
        role=AdminRole.ADMIN,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


# ── user usecase fixtures ──────────────────────

@pytest.fixture
def valid_user_data():
    return {
        "first_name": "Ana",
        "last_name": "Silva",
        "username": "ana.silva",
        "email": "ana.silva@example.com",
        "password": "Senha@123",
        "role": AdminRole.ADMIN,
    }


@pytest.fixture
def fake_user_domain():
    return Admin(
        id=uuid4(),
        first_name="Ana",
        last_name="Silva",
        username="ana.silva",
        email="ana.silva@example.com",
        password="hashed_password",
        role=AdminRole.ADMIN,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def current_user(fake_user_domain):
    return AdminResponse(
        id=fake_user_domain.id,
        first_name=fake_user_domain.first_name,
        last_name=fake_user_domain.last_name,
        email=fake_user_domain.email,
        username=fake_user_domain.username,
        role=fake_user_domain.role,
        created_at=fake_user_domain.created_at,
        updated_at=fake_user_domain.updated_at,
    )
