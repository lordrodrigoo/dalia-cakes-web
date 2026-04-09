# pylint: disable=redefined-outer-name
from uuid import uuid4
from datetime import datetime
from unittest.mock import MagicMock
import pytest
from backend.src.domain.models.user import Users, UserRole
from backend.src.dto.response.user_response import UserResponse
from backend.src.usecases.user_usecases import UserUsecase
from backend.src.usecases.auth_usecases import AuthUsecase
from backend.src.config.security import hash_password


@pytest.fixture
def user_repository_mock():
    return MagicMock()


@pytest.fixture
def usecase(user_repository_mock):
    return UserUsecase(user_repository_mock)


# ── auth fixtures ──────────────────────────────

@pytest.fixture
def auth_repository_mock():
    return MagicMock()


@pytest.fixture
def auth_usecase(auth_repository_mock):
    return AuthUsecase(auth_repository_mock)


@pytest.fixture
def fake_auth_user():
    return Users(
        id=uuid4(),
        first_name="Rodrigo",
        last_name="Souza",
        username="rodrigo.souza",
        email="rodrigo@example.com",
        password=hash_password("P@ssw0rd1"),
        role=UserRole.ADMIN,
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
        "role": UserRole.ADMIN,
    }


@pytest.fixture
def fake_user_domain():
    return Users(
        id=uuid4(),
        first_name="Ana",
        last_name="Silva",
        username="ana.silva",
        email="ana.silva@example.com",
        password="hashed_password",
        role=UserRole.ADMIN,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def current_user(fake_user_domain):
    return UserResponse(
        id=fake_user_domain.id,
        first_name=fake_user_domain.first_name,
        last_name=fake_user_domain.last_name,
        email=fake_user_domain.email,
        username=fake_user_domain.username,
        role=fake_user_domain.role,
        created_at=fake_user_domain.created_at,
        updated_at=fake_user_domain.updated_at,
    )
