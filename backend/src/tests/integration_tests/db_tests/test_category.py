# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
import pytest
from backend.src.infra.db.entities.category import CategoryEntity


def test_insert_category(db_session, fake_category):
    assert fake_category.id is not None
    assert fake_category.name == "Bolos Decorados"
    assert fake_category.slug == "bolos-decorados"


def test_update_category(db_session, fake_category):
    fake_category.name = "Cupcakes"
    db_session.commit()
    updated = db_session.query(CategoryEntity).filter_by(id=fake_category.id).first()
    assert updated.name == "Cupcakes"


def test_delete_category(db_session, fake_category):
    db_session.delete(fake_category)
    db_session.commit()
    deleted = db_session.query(CategoryEntity).filter_by(id=fake_category.id).first()
    assert deleted is None


def test_find_category_by_id(db_session, fake_category):
    found = db_session.query(CategoryEntity).filter_by(id=fake_category.id).first()
    assert found is not None


def test_find_all_categories(db_session, fake_category):
    categories = db_session.query(CategoryEntity).all()
    assert len(categories) >= 1


def test_unique_category_name(db_session, fake_category):
    duplicate = CategoryEntity(
        name="Bolos Decorados",  # nome duplicado
        slug="outro-slug",
    )
    db_session.add(duplicate)
    with pytest.raises(Exception):
        db_session.commit()


def test_unique_category_slug(db_session, fake_category):
    duplicate = CategoryEntity(
        name="Outro Nome",
        slug="bolos-decorados",  # slug duplicado
    )
    db_session.add(duplicate)
    with pytest.raises(Exception):
        db_session.commit()
