# pylint: disable=redefined-outer-name
from decimal import Decimal
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from backend.src.infra.db.settings.base import Base
from backend.src.infra.db.entities.admin import AdminEntity
from backend.src.infra.db.entities.category import CategoryEntity
from backend.src.infra.db.entities.product import ProductEntity
from backend.src.config.security import hash_password


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

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


@pytest.fixture(scope="function")
def fake_category(db_session):
    category = CategoryEntity(
        name="Bolos Decorados",
        slug="bolos-decorados",
        image_url="https://example.com/bolos.jpg",
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture(scope="function")
def fake_product(db_session, fake_category):
    product = ProductEntity(
        name="Bolo de Cenoura",
        price=Decimal("45.90"),
        image_url="https://example.com/bolo.jpg",
        category_id=fake_category.id,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product
