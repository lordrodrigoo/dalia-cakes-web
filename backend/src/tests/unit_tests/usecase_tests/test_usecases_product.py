# pylint: disable=redefined-outer-name
from uuid import uuid4
import pytest
from backend.src.dto.request.product_request import ProductRequest
from backend.src.exceptions.exception_handlers_product import (
    ProductNotFoundException,
    ProductCategoryNotFoundException,
)


# ──────────────────────────────────────────────
# create_product
# ──────────────────────────────────────────────

def test_create_product_success(product_usecase, product_repository_mock, category_repository_mock, valid_product_data, fake_product_domain, fake_category_domain):
    category_repository_mock.get_category_by_id.return_value = fake_category_domain
    product_repository_mock.create_product.return_value = fake_product_domain

    request = ProductRequest(**valid_product_data)
    result = product_usecase.create_product(request)

    assert result.name == fake_product_domain.name
    product_repository_mock.create_product.assert_called_once()


def test_create_product_category_not_found(product_usecase, category_repository_mock, valid_product_data):
    category_repository_mock.get_category_by_id.return_value = None

    request = ProductRequest(**valid_product_data)
    with pytest.raises(ProductCategoryNotFoundException) as exc_info:
        product_usecase.create_product(request)

    assert str(valid_product_data["category_id"]) in exc_info.value.message


# ──────────────────────────────────────────────
# get_product_by_id
# ──────────────────────────────────────────────

def test_get_product_by_id_success(product_usecase, product_repository_mock, fake_product_domain):
    product_repository_mock.get_product_by_id.return_value = fake_product_domain

    result = product_usecase.get_product_by_id(fake_product_domain.id)

    assert result.id == fake_product_domain.id
    product_repository_mock.get_product_by_id.assert_called_once_with(fake_product_domain.id)


def test_get_product_by_id_not_found(product_usecase, product_repository_mock):
    product_repository_mock.get_product_by_id.return_value = None

    with pytest.raises(ProductNotFoundException):
        product_usecase.get_product_by_id(uuid4())


# ──────────────────────────────────────────────
# get_all_products
# ──────────────────────────────────────────────

def test_get_all_products(product_usecase, product_repository_mock, fake_product_domain):
    product_repository_mock.get_all_products.return_value = [fake_product_domain]

    result = product_usecase.get_all_products()

    assert len(result) == 1
    assert result[0].name == fake_product_domain.name


def test_get_all_products_empty(product_usecase, product_repository_mock):
    product_repository_mock.get_all_products.return_value = []

    result = product_usecase.get_all_products()

    assert result == []


# ──────────────────────────────────────────────
# get_products_by_category
# ──────────────────────────────────────────────

def test_get_products_by_category_success(product_usecase, product_repository_mock, category_repository_mock, fake_product_domain, fake_category_domain):
    category_repository_mock.get_category_by_id.return_value = fake_category_domain
    product_repository_mock.get_products_by_category.return_value = [fake_product_domain]

    result = product_usecase.get_products_by_category(fake_category_domain.id)

    assert len(result) == 1


def test_get_products_by_category_not_found(product_usecase, category_repository_mock):
    category_repository_mock.get_category_by_id.return_value = None

    with pytest.raises(ProductCategoryNotFoundException):
        product_usecase.get_products_by_category(uuid4())


# ──────────────────────────────────────────────
# update_product
# ──────────────────────────────────────────────

def test_update_product_success(product_usecase, product_repository_mock, valid_product_data, fake_product_domain):
    product_repository_mock.get_product_by_id.return_value = fake_product_domain
    product_repository_mock.update_product.return_value = fake_product_domain

    request = ProductRequest(**valid_product_data)
    result = product_usecase.update_product(fake_product_domain.id, request)

    assert result.id == fake_product_domain.id
    product_repository_mock.update_product.assert_called_once()


def test_update_product_not_found(product_usecase, product_repository_mock, valid_product_data):
    product_repository_mock.get_product_by_id.return_value = None

    request = ProductRequest(**valid_product_data)
    with pytest.raises(ProductNotFoundException):
        product_usecase.update_product(uuid4(), request)


def test_update_product_category_changed_not_found(product_usecase, product_repository_mock, category_repository_mock, valid_product_data, fake_product_domain):
    new_category_id = uuid4()
    valid_product_data["category_id"] = new_category_id  # different from fake_product_domain.category_id
    fake_product_domain.category_id = uuid4()  # ensure they differ

    product_repository_mock.get_product_by_id.return_value = fake_product_domain
    category_repository_mock.get_category_by_id.return_value = None

    request = ProductRequest(**valid_product_data)
    with pytest.raises(ProductCategoryNotFoundException):
        product_usecase.update_product(fake_product_domain.id, request)


def test_update_product_category_changed_success(product_usecase, product_repository_mock, category_repository_mock, valid_product_data, fake_product_domain, fake_category_domain):
    new_category_id = uuid4()
    valid_product_data["category_id"] = new_category_id
    fake_product_domain.category_id = uuid4()  # different from new_category_id

    product_repository_mock.get_product_by_id.return_value = fake_product_domain
    category_repository_mock.get_category_by_id.return_value = fake_category_domain
    product_repository_mock.update_product.return_value = fake_product_domain

    request = ProductRequest(**valid_product_data)
    result = product_usecase.update_product(fake_product_domain.id, request)

    assert result is not None
    category_repository_mock.get_category_by_id.assert_called_once_with(new_category_id)


# ──────────────────────────────────────────────
# delete_product
# ──────────────────────────────────────────────

def test_delete_product_success(product_usecase, product_repository_mock, fake_product_domain):
    product_repository_mock.get_product_by_id.return_value = fake_product_domain

    product_usecase.delete_product(fake_product_domain.id)

    product_repository_mock.delete_product.assert_called_once_with(fake_product_domain.id)


def test_delete_product_not_found(product_usecase, product_repository_mock):
    product_repository_mock.get_product_by_id.return_value = None

    with pytest.raises(ProductNotFoundException):
        product_usecase.delete_product(uuid4())
