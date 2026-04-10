# pylint: disable=redefined-outer-name
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.infra.db.settings.base import Base
from backend.src.infra.db.entities.admin import AdminEntity
from backend.src.config.security import hash_password


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def fake_user(db_session):
    user = AdminEntity(
        first_name="Ana",
        last_name="Silva",
        username="ana.silva",
        email="ana.silva@example.com",
        password=hash_password("password123"),
        role="admin",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
