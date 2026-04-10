import uuid
from datetime import datetime
from backend.src.infra.db.entities.category import CategoryEntity
from backend.src.domain.models.category import Category


def test_category_entity_repr():
    entity = CategoryEntity(
        id=uuid.uuid4(),
        name="Bolos Decorados",
        slug="bolos-decorados",
        image_url="https://example.com/bolos.jpg",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    result = repr(entity)
    assert "CategoryEntity" in result
    assert "Bolos Decorados" in result
    assert "bolos-decorados" in result


def test_category_from_entity():
    entity = CategoryEntity(
        id=uuid.uuid4(),
        name="Bolos Decorados",
        slug="bolos-decorados",
        image_url="https://example.com/bolos.jpg",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    category = Category.from_entity(entity)
    assert category.id == entity.id
    assert category.name == entity.name
    assert category.slug == entity.slug
    assert category.image_url == entity.image_url


def test_category_create_category():
    category = Category.create_category(
        name="Cupcakes",
        slug="cupcakes",
        image_url="https://example.com/cupcakes.jpg",
    )
    assert category.name == "Cupcakes"
    assert category.slug == "cupcakes"
    assert category.image_url == "https://example.com/cupcakes.jpg"


def test_category_create_category_no_image():
    category = Category.create_category(name="Brigadeiros", slug="brigadeiros")
    assert category.image_url is None


def test_category_repr():
    category = Category(
        name="Bolos Decorados",
        slug="bolos-decorados",
        id=uuid.uuid4(),
    )
    result = repr(category)
    assert "Category" in result
    assert "Bolos Decorados" in result
    assert "bolos-decorados" in result
