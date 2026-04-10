# pylint: disable=redefined-outer-name
from uuid import uuid4
import pytest
from backend.src.dto.request.category_request import CategoryRequest
from backend.src.exceptions.exception_handlers_category import (
    CategoryNotFoundException,
    CategoryNameAlreadyExistsException,
    CategorySlugAlreadyExistsException,
)


# ──────────────────────────────────────────────
# create_category
# ──────────────────────────────────────────────

def test_create_category_success(category_usecase, category_repository_mock, valid_category_data, fake_category_domain):
    category_repository_mock.get_category_by_slug.return_value = None
    category_repository_mock.get_category_by_name.return_value = None
    category_repository_mock.create_category.return_value = fake_category_domain

    request = CategoryRequest(**valid_category_data)
    result = category_usecase.create_category(request)

    assert result.name == fake_category_domain.name
    assert result.slug == fake_category_domain.slug
    category_repository_mock.create_category.assert_called_once()


def test_create_category_slug_conflict(category_usecase, category_repository_mock, valid_category_data, fake_category_domain):
    category_repository_mock.get_category_by_slug.return_value = fake_category_domain

    request = CategoryRequest(**valid_category_data)
    with pytest.raises(CategorySlugAlreadyExistsException) as exc_info:
        category_usecase.create_category(request)

    assert valid_category_data["slug"] in exc_info.value.message


def test_create_category_name_conflict(category_usecase, category_repository_mock, valid_category_data, fake_category_domain):
    category_repository_mock.get_category_by_slug.return_value = None
    category_repository_mock.get_category_by_name.return_value = fake_category_domain

    request = CategoryRequest(**valid_category_data)
    with pytest.raises(CategoryNameAlreadyExistsException) as exc_info:
        category_usecase.create_category(request)

    assert valid_category_data["name"] in exc_info.value.message


# ──────────────────────────────────────────────
# get_category_by_id
# ──────────────────────────────────────────────

def test_get_category_by_id_success(category_usecase, category_repository_mock, fake_category_domain):
    category_repository_mock.get_category_by_id.return_value = fake_category_domain

    result = category_usecase.get_category_by_id(fake_category_domain.id)

    assert result.id == fake_category_domain.id
    category_repository_mock.get_category_by_id.assert_called_once_with(fake_category_domain.id)


def test_get_category_by_id_not_found(category_usecase, category_repository_mock):
    category_repository_mock.get_category_by_id.return_value = None

    with pytest.raises(CategoryNotFoundException):
        category_usecase.get_category_by_id(uuid4())


# ──────────────────────────────────────────────
# get_category_by_slug
# ──────────────────────────────────────────────

def test_get_category_by_slug_success(category_usecase, category_repository_mock, fake_category_domain):
    category_repository_mock.get_category_by_slug.return_value = fake_category_domain

    result = category_usecase.get_category_by_slug(fake_category_domain.slug)

    assert result.slug == fake_category_domain.slug


def test_get_category_by_slug_not_found(category_usecase, category_repository_mock):
    category_repository_mock.get_category_by_slug.return_value = None

    with pytest.raises(CategoryNotFoundException) as exc_info:
        category_usecase.get_category_by_slug("nao-existe")

    assert "nao-existe" in exc_info.value.message


# ──────────────────────────────────────────────
# get_all_categories
# ──────────────────────────────────────────────

def test_get_all_categories(category_usecase, category_repository_mock, fake_category_domain):
    category_repository_mock.get_all_categories.return_value = [fake_category_domain]

    result = category_usecase.get_all_categories()

    assert len(result) == 1
    assert result[0].name == fake_category_domain.name


def test_get_all_categories_empty(category_usecase, category_repository_mock):
    category_repository_mock.get_all_categories.return_value = []

    result = category_usecase.get_all_categories()

    assert result == []


# ──────────────────────────────────────────────
# update_category
# ──────────────────────────────────────────────

def test_update_category_success(category_usecase, category_repository_mock, valid_category_data, fake_category_domain):
    category_repository_mock.get_category_by_id.return_value = fake_category_domain
    category_repository_mock.update_category.return_value = fake_category_domain

    request = CategoryRequest(**valid_category_data)
    result = category_usecase.update_category(fake_category_domain.id, request)

    assert result.id == fake_category_domain.id
    category_repository_mock.update_category.assert_called_once()


def test_update_category_not_found(category_usecase, category_repository_mock, valid_category_data):
    category_repository_mock.get_category_by_id.return_value = None

    request = CategoryRequest(**valid_category_data)
    with pytest.raises(CategoryNotFoundException):
        category_usecase.update_category(uuid4(), request)


def test_update_category_name_conflict(category_usecase, category_repository_mock, valid_category_data, fake_category_domain):
    # Change the name on the stored category so diff is detected
    stored = fake_category_domain
    stored.name = "Nome Antigo"
    category_repository_mock.get_category_by_id.return_value = stored
    category_repository_mock.get_category_by_name.return_value = fake_category_domain  # conflict

    request = CategoryRequest(**valid_category_data)
    with pytest.raises(CategoryNameAlreadyExistsException):
        category_usecase.update_category(stored.id, request)


def test_update_category_slug_conflict(category_usecase, category_repository_mock, valid_category_data, fake_category_domain):
    stored = fake_category_domain
    stored.slug = "slug-antigo"
    category_repository_mock.get_category_by_id.return_value = stored
    category_repository_mock.get_category_by_name.return_value = None
    category_repository_mock.get_category_by_slug.return_value = fake_category_domain  # conflict

    request = CategoryRequest(**valid_category_data)
    with pytest.raises(CategorySlugAlreadyExistsException):
        category_usecase.update_category(stored.id, request)


# ──────────────────────────────────────────────
# delete_category
# ──────────────────────────────────────────────

def test_delete_category_success(category_usecase, category_repository_mock, fake_category_domain):
    category_repository_mock.get_category_by_id.return_value = fake_category_domain

    category_usecase.delete_category(fake_category_domain.id)

    category_repository_mock.delete_category.assert_called_once_with(fake_category_domain.id)


def test_delete_category_not_found(category_usecase, category_repository_mock):
    category_repository_mock.get_category_by_id.return_value = None

    with pytest.raises(CategoryNotFoundException):
        category_usecase.delete_category(uuid4())
