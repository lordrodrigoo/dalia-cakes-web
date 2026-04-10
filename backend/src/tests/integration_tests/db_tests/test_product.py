# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
import uuid
from decimal import Decimal
import pytest
from backend.src.infra.db.entities.product import ProductEntity


def test_insert_product(db_session, fake_product, fake_category):
    assert fake_product.id is not None
    assert fake_product.name == "Bolo de Cenoura"
    assert fake_product.category_id == fake_category.id


def test_update_product(db_session, fake_product):
    fake_product.name = "Bolo de Limão"
    db_session.commit()
    updated = db_session.query(ProductEntity).filter_by(id=fake_product.id).first()
    assert updated.name == "Bolo de Limão"


def test_delete_product(db_session, fake_product):
    db_session.delete(fake_product)
    db_session.commit()
    deleted = db_session.query(ProductEntity).filter_by(id=fake_product.id).first()
    assert deleted is None


def test_find_product_by_id(db_session, fake_product):
    found = db_session.query(ProductEntity).filter_by(id=fake_product.id).first()
    assert found is not None


def test_find_all_products(db_session, fake_product):
    products = db_session.query(ProductEntity).all()
    assert len(products) >= 1


def test_product_fk_constraint(db_session):
    """Produto sem category_id válido deve falhar."""
    product = ProductEntity(
        name="Bolo Sem Categoria",
        price=Decimal("30.00"),
        category_id=uuid.uuid4(),  # FK inexistente
    )
    db_session.add(product)
    with pytest.raises(Exception):
        db_session.commit()
