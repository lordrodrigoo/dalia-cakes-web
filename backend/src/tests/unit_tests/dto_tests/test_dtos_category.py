# pylint: disable=redefined-outer-name
from uuid import uuid4
from datetime import datetime
import pytest
from pydantic import ValidationError
from backend.src.dto.request.category_request import CategoryRequest
from backend.src.dto.response.category_response import CategoryResponse


# ──────────────────────────────────────────────
# fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def valid_category_data():
    return {
        "name": "Bolos Decorados",
        "slug": "bolos-decorados",
        "image_url": "https://example.com/bolos.jpg",
    }


# ──────────────────────────────────────────────
# CategoryRequest — campo válido
# ──────────────────────────────────────────────

def test_valid_category_request(valid_category_data):
    req = CategoryRequest(**valid_category_data)
    assert req.name == "Bolos Decorados"
    assert req.slug == "bolos-decorados"
    assert req.image_url == valid_category_data["image_url"]


def test_category_request_image_url_optional(valid_category_data):
    valid_category_data.pop("image_url")
    req = CategoryRequest(**valid_category_data)
    assert req.image_url is None


def test_category_request_name_strip(valid_category_data):
    valid_category_data["name"] = "  Bolos  "
    req = CategoryRequest(**valid_category_data)
    assert req.name == "Bolos"


# ──────────────────────────────────────────────
# CategoryRequest — validações de campo
# ──────────────────────────────────────────────

@pytest.mark.parametrize("field,value,expected_msg", [
    ("name", "ab", "String should have at least 3 characters"),
    ("name", "a" * 51, "String should have at most 50 characters"),
    ("slug", "ab", "String should have at least 3 characters"),
    ("slug", "Bolos-Decorados", "slug must be lowercase"),
    ("slug", "bolos decorados", "slug must be lowercase"),
    ("slug", "bolos_decorados", "slug must be lowercase"),
    ("image_url", "x" * 501, "String should have at most 500 characters"),
])
def test_category_request_field_validations(valid_category_data, field, value, expected_msg):
    data = valid_category_data.copy()
    data[field] = value
    with pytest.raises(ValidationError) as exc_info:
        CategoryRequest(**data)
    assert expected_msg in str(exc_info.value)


# ──────────────────────────────────────────────
# CategoryResponse
# ──────────────────────────────────────────────

def test_valid_category_response():
    now = datetime.now()
    resp = CategoryResponse(
        id=uuid4(),
        name="Bolos Decorados",
        slug="bolos-decorados",
        image_url="https://example.com/bolos.jpg",
        created_at=now,
        updated_at=now,
    )
    assert resp.name == "Bolos Decorados"
    assert resp.slug == "bolos-decorados"


def test_category_response_image_url_optional():
    now = datetime.now()
    resp = CategoryResponse(
        id=uuid4(),
        name="Bolos Decorados",
        slug="bolos-decorados",
        created_at=now,
        updated_at=now,
    )
    assert resp.image_url is None
