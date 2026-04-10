# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
from uuid import uuid4
from backend.src.domain.models.category import Category
from backend.src.infra.db.repositories.category_repository_interface import CategoryRepository
from backend.src.tests.helpers import FakeDBConnectionHandler


# ──────────────────────────────────────────────
# create_category
# ──────────────────────────────────────────────

def test_create_category(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = CategoryRepository(db_handler)

    category = Category.create_category(
        name="Bolos Decorados",
        slug="bolos-decorados",
        image_url="https://example.com/bolos.jpg",
    )
    created = repo.create_category(category)
    db_session.commit()

    assert created.id is not None
    assert created.name == "Bolos Decorados"
    assert created.slug == "bolos-decorados"


# ──────────────────────────────────────────────
# update_category
# ──────────────────────────────────────────────

def test_update_category(fake_category, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = CategoryRepository(db_handler)

    category = Category.from_entity(fake_category)
    category.name = "Cupcakes"
    category.slug = "cupcakes"

    updated = repo.update_category(category)
    db_session.commit()

    assert updated.name == "Cupcakes"
    assert updated.slug == "cupcakes"


def test_update_category_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = CategoryRepository(db_handler)

    category = Category(
        id=uuid4(),
        name="Fantasma",
        slug="fantasma",
    )
    result = repo.update_category(category)
    assert result is None


# ──────────────────────────────────────────────
# delete_category
# ──────────────────────────────────────────────

def test_delete_category(fake_category, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = CategoryRepository(db_handler)

    repo.delete_category(fake_category.id)
    db_session.commit()

    result = repo.get_category_by_id(fake_category.id)
    assert result is None


# ──────────────────────────────────────────────
# get_category_by_id
# ──────────────────────────────────────────────

def test_get_category_by_id(fake_category, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = CategoryRepository(db_handler)

    found = repo.get_category_by_id(fake_category.id)
    assert found is not None
    assert found.id == fake_category.id


def test_get_category_by_id_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = CategoryRepository(db_handler)

    result = repo.get_category_by_id(uuid4())
    assert result is None


# ──────────────────────────────────────────────
# get_category_by_slug
# ──────────────────────────────────────────────

def test_get_category_by_slug(fake_category, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = CategoryRepository(db_handler)

    found = repo.get_category_by_slug("bolos-decorados")
    assert found is not None
    assert found.slug == "bolos-decorados"


def test_get_category_by_slug_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = CategoryRepository(db_handler)

    result = repo.get_category_by_slug("nao-existe")
    assert result is None


# ──────────────────────────────────────────────
# get_category_by_name
# ──────────────────────────────────────────────

def test_get_category_by_name(fake_category, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = CategoryRepository(db_handler)

    found = repo.get_category_by_name("Bolos Decorados")
    assert found is not None
    assert found.name == "Bolos Decorados"


def test_get_category_by_name_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = CategoryRepository(db_handler)

    result = repo.get_category_by_name("Inexistente")
    assert result is None


# ──────────────────────────────────────────────
# get_all_categories
# ──────────────────────────────────────────────

def test_get_all_categories(fake_category, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = CategoryRepository(db_handler)

    result = repo.get_all_categories()
    assert len(result) >= 1


def test_get_all_categories_empty(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = CategoryRepository(db_handler)

    result = repo.get_all_categories()
    assert result == []
