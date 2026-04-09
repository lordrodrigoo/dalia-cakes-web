# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
from uuid import uuid4
from backend.src.domain.models.user import Users, UserRole
from backend.src.infra.db.repositories.user_repository_interface import UserRepository
from backend.src.tests.helpers import FakeDBConnectionHandler
from backend.src.config.security import hash_password


# ──────────────────────────────────────────────
# create_user
# ──────────────────────────────────────────────

def test_create_user(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    user = Users.create_user(
        first_name="Carlos",
        last_name="Pereira",
        username="carlos.pereira",
        email="carlos@example.com",
        password=hash_password("senha123"),
    )
    created = user_repo.create_user(user)
    db_session.commit()

    assert created.id is not None
    assert created.first_name == "Carlos"
    assert created.email == "carlos@example.com"
    assert created.role == UserRole.ADMIN


# ──────────────────────────────────────────────
# update_user
# ──────────────────────────────────────────────

def test_update_user(fake_user, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    user = Users.from_entity(fake_user)
    user.first_name = "Ana Updated"
    user.last_name = "Silva Updated"
    user.email = "ana.updated@example.com"
    user.role = UserRole.OWNER

    updated = user_repo.update_user(user)
    db_session.commit()

    assert updated.first_name == "Ana Updated"
    assert updated.last_name == "Silva Updated"
    assert updated.email == "ana.updated@example.com"
    assert updated.role == UserRole.OWNER


def test_update_user_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    user = Users(
        id=uuid4(),
        first_name="Ghost",
        last_name="User",
        username="ghost",
        email="ghost@example.com",
        password="x",
    )
    result = user_repo.update_user(user)
    assert result is None


# ──────────────────────────────────────────────
# get_user_by_id
# ──────────────────────────────────────────────

def test_get_user_by_id(fake_user, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    found = user_repo.get_user_by_id(fake_user.id)
    assert found is not None
    assert found.id == fake_user.id


def test_get_user_by_id_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    result = user_repo.get_user_by_id(uuid4())
    assert result is None


# ──────────────────────────────────────────────
# delete_user
# ──────────────────────────────────────────────

def test_delete_user(fake_user, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    user_repo.delete_user(fake_user.id)
    db_session.commit()

    result = user_repo.get_user_by_id(fake_user.id)
    assert result is None


# ──────────────────────────────────────────────
# get_user_by_email
# ──────────────────────────────────────────────

def test_get_user_by_email(fake_user, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    found = user_repo.get_user_by_email("ana.silva@example.com")
    assert found is not None
    assert found.email == "ana.silva@example.com"


def test_get_user_by_email_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    result = user_repo.get_user_by_email("naoexiste@example.com")
    assert result is None


# ──────────────────────────────────────────────
# get_user_by_username
# ──────────────────────────────────────────────

def test_get_user_by_username(fake_user, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    found = user_repo.get_user_by_username("ana.silva")
    assert found is not None
    assert found.username == "ana.silva"


def test_get_user_by_username_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    user_repo = UserRepository(db_handler)

    result = user_repo.get_user_by_username("naoexiste")
    assert result is None
