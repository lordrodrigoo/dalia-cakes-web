# pylint: disable=redefined-outer-name
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from unittest.mock import MagicMock
import pytest
from backend.src.domain.models.admin import Admin, AdminRole
from backend.src.domain.models.category import Category
from backend.src.domain.models.decorated_cake import DecoratedCake
from backend.src.domain.models.instagram_post import InstagramPost
from backend.src.domain.models.product import Product
from backend.src.dto.response.admin_response import AdminResponse
from backend.src.usecases.admin_usecases import AdminUsecase
from backend.src.usecases.auth_usecases import AuthUsecase
from backend.src.usecases.category_usecases import CategoryUsecase
from backend.src.usecases.chatbot_usecases import ChatbotUsecase
from backend.src.usecases.instagram_usecases import InstagramPostUsecase
from backend.src.usecases.product_usecases import ProductUsecase
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


# ──────────────────────────────────────────────
# Category fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def category_repository_mock():
    return MagicMock()


@pytest.fixture
def category_usecase(category_repository_mock):
    return CategoryUsecase(category_repository_mock)


@pytest.fixture
def fake_category_domain():
    return Category(
        id=uuid4(),
        name="Bolos Decorados",
        slug="bolos-decorados",
        image_url="https://example.com/bolos.jpg",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def valid_category_data():
    return {
        "name": "Bolos Decorados",
        "slug": "bolos-decorados",
        "image_url": "https://example.com/bolos.jpg",
    }


# ──────────────────────────────────────────────
# Product fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def product_repository_mock():
    return MagicMock()


@pytest.fixture
def product_usecase(product_repository_mock, category_repository_mock):
    return ProductUsecase(product_repository_mock, category_repository_mock)


@pytest.fixture
def fake_product_domain(fake_category_domain):
    return Product(
        id=uuid4(),
        name="Bolo de Cenoura",
        price=Decimal("45.90"),
        image_url="https://example.com/bolo.jpg",
        category_id=fake_category_domain.id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def valid_product_data(fake_category_domain):
    return {
        "name": "Bolo de Cenoura",
        "price": Decimal("45.90"),
        "category_id": fake_category_domain.id,
        "image_url": "https://example.com/bolo.jpg",
    }


# ──────────────────────────────────────────────
# Instagram fixtures
# ──────────────────────────────────────────────


@pytest.fixture
def instagram_post_repository_mock():
    return MagicMock()


@pytest.fixture
def decorated_cake_repository_mock():
    return MagicMock()


@pytest.fixture
def instagram_usecase(instagram_post_repository_mock, decorated_cake_repository_mock):
    return InstagramPostUsecase(instagram_post_repository_mock, decorated_cake_repository_mock)


@pytest.fixture
def fake_decorated_cake_domain():
    return DecoratedCake(
        id=uuid4(),
        name="Feminino",
        slug="feminino",
        hashtag="feminino",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def fake_instagram_post_domain(fake_decorated_cake_domain):
    now = datetime.now(timezone.utc)
    return InstagramPost(
        id=uuid4(),
        instagram_id="123456789",
        caption="Bolo lindo #feminino",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
        subcategory_id=fake_decorated_cake_domain.id,
        is_featured=True,
        synced_at=now,
        featured_until=now + timedelta(days=3),
        created_at=now,
        updated_at=now,
    )


# ──────────────────────────────────────────────
# Chatbot fixtures
# ──────────────────────────────────────────────


@pytest.fixture
def gemini_client_mock():
    return MagicMock()


@pytest.fixture
def chatbot_usecase(product_repository_mock, category_repository_mock, gemini_client_mock):
    return ChatbotUsecase(product_repository_mock, category_repository_mock, gemini_client_mock)
