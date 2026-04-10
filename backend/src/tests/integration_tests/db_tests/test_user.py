#pylint: disable=redefined-outer-name
#pylint: disable=unused-argument
import pytest
from backend.src.infra.db.entities.admin import AdminEntity
from backend.src.config.security import hash_password


def test_insert_user(db_session, fake_user):
    assert fake_user.id is not None
    assert fake_user.first_name == "Ana"
    assert fake_user.last_name == "Silva"
    assert fake_user.email == "ana.silva@example.com"

def test_update_admin(db_session, fake_user):
    fake_user.last_name = "Souza"
    db_session.commit()
    updated_user = db_session.query(AdminEntity).filter_by(id=fake_user.id).first()
    assert updated_user.last_name == "Souza"

def test_delete_admin(db_session, fake_user):
    db_session.delete(fake_user)
    db_session.commit()
    deleted_user = db_session.query(AdminEntity).filter_by(id=fake_user.id).first()
    assert deleted_user is None

def test_find_user_by_id(db_session, fake_user):
    found_user = db_session.query(AdminEntity).filter_by(id=fake_user.id).first()
    assert found_user is not None

def test_find_all_users(db_session, fake_user):
    users = db_session.query(AdminEntity).all()
    assert len(users) >= 1

def test_unique_email(db_session, fake_user):
    duplicate = AdminEntity(
        first_name="Carlos",
        last_name="Pereira",
        username="carlos.pereira",
        email="ana.silva@example.com",  # email duplicado
        password=hash_password("password456"),
        role="admin",
    )
    db_session.add(duplicate)
    with pytest.raises(Exception):
        db_session.commit()

def test_unique_username(db_session, fake_user):
    duplicate = AdminEntity(
        first_name="Carlos",
        last_name="Pereira",
        username="ana.silva",  # username duplicado
        email="carlos@example.com",
        password=hash_password("password456"),
        role="admin",
    )
    db_session.add(duplicate)
    with pytest.raises(Exception):
        db_session.commit()

def test_user_role(db_session, fake_user):
    assert fake_user.role == "admin"
