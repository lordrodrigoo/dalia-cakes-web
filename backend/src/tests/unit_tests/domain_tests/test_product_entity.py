import uuid
from datetime import datetime
from decimal import Decimal
from backend.src.infra.db.entities.product import ProductEntity
from backend.src.domain.models.product import Product


def test_product_entity_repr():
    entity = ProductEntity(
        id=uuid.uuid4(),
        name="Bolo de Cenoura",
        price=Decimal("45.90"),
        image_url="https://example.com/bolo.jpg",
        category_id=uuid.uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    result = repr(entity)
    assert "ProductEntity" in result
    assert "Bolo de Cenoura" in result


def test_product_from_entity():
    entity = ProductEntity(
        id=uuid.uuid4(),
        name="Bolo de Cenoura",
        price=Decimal("45.90"),
        image_url="https://example.com/bolo.jpg",
        category_id=uuid.uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    product = Product.from_entity(entity)
    assert product.id == entity.id
    assert product.name == entity.name
    assert product.price == entity.price
    assert product.category_id == entity.category_id


def test_product_full_description():
    product = Product(
        name="Bolo de Cenoura",
        price=Decimal("45.90"),
        category_id=uuid.uuid4(),
    )
    assert product.full_description == "Bolo de Cenoura - $45.90"


def test_product_create_product():
    category_id = uuid.uuid4()
    product = Product.create_product(
        name="Bolo de Limão",
        image_url="https://example.com/limao.jpg",
        price=Decimal("39.90"),
        category_id=category_id,
    )
    assert product.name == "Bolo de Limão"
    assert product.price == Decimal("39.90")
    assert product.category_id == category_id


def test_product_repr():
    product = Product(
        name="Bolo de Cenoura",
        price=Decimal("45.90"),
        category_id=uuid.uuid4(),
        id=uuid.uuid4(),
    )
    result = repr(product)
    assert "Product" in result
    assert "Bolo de Cenoura" in result
