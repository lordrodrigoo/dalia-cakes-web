# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
from uuid import uuid4
from decimal import Decimal
from backend.src.domain.models.product import Product
from backend.src.infra.db.repositories.product_repository_interface import ProductRepository
from backend.src.tests.helpers import FakeDBConnectionHandler


# ──────────────────────────────────────────────
# create_product
# ──────────────────────────────────────────────

def test_create_product(fake_category, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = ProductRepository(db_handler)

    product = Product.create_product(
        name="Bolo de Cenoura",
        price=Decimal("45.90"),
        image_url="https://example.com/bolo.jpg",
        category_id=fake_category.id,
    )
    created = repo.create_product(product)
    db_session.commit()

    assert created.id is not None
    assert created.name == "Bolo de Cenoura"
    assert created.category_id == fake_category.id


# ──────────────────────────────────────────────
# update_product
# ──────────────────────────────────────────────

def test_update_product(fake_product, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = ProductRepository(db_handler)

    product = Product.from_entity(fake_product)
    product.name = "Bolo de Limão"
    product.price = Decimal("39.90")

    updated = repo.update_product(product)
    db_session.commit()

    assert updated.name == "Bolo de Limão"
    assert updated.price == Decimal("39.90")


def test_update_product_not_found(db_session, fake_category):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = ProductRepository(db_handler)

    product = Product(
        id=uuid4(),
        name="Fantasma",
        price=Decimal("10.00"),
        category_id=fake_category.id,
    )
    result = repo.update_product(product)
    assert result is None


# ──────────────────────────────────────────────
# delete_product
# ──────────────────────────────────────────────

def test_delete_product(fake_product, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = ProductRepository(db_handler)

    repo.delete_product(fake_product.id)
    db_session.commit()

    result = repo.get_product_by_id(fake_product.id)
    assert result is None


# ──────────────────────────────────────────────
# get_product_by_id
# ──────────────────────────────────────────────

def test_get_product_by_id(fake_product, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = ProductRepository(db_handler)

    found = repo.get_product_by_id(fake_product.id)
    assert found is not None
    assert found.id == fake_product.id


def test_get_product_by_id_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = ProductRepository(db_handler)

    result = repo.get_product_by_id(uuid4())
    assert result is None


# ──────────────────────────────────────────────
# get_all_products
# ──────────────────────────────────────────────

def test_get_all_products(fake_product, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = ProductRepository(db_handler)

    result = repo.get_all_products()
    assert len(result) >= 1


def test_get_all_products_empty(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = ProductRepository(db_handler)

    result = repo.get_all_products()
    assert result == []


# ──────────────────────────────────────────────
# get_products_by_category
# ──────────────────────────────────────────────

def test_get_products_by_category(fake_product, fake_category, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = ProductRepository(db_handler)

    result = repo.get_products_by_category(fake_category.id)
    assert len(result) >= 1
    assert all(p.category_id == fake_category.id for p in result)


def test_get_products_by_category_empty(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = ProductRepository(db_handler)

    result = repo.get_products_by_category(uuid4())
    assert result == []
