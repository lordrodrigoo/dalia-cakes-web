# pylint: disable=redefined-outer-name
from uuid import uuid4
from datetime import datetime
from decimal import Decimal
import pytest
from pydantic import ValidationError as PydanticValidationError
from backend.src.dto.request.product_request import ProductRequest
from backend.src.dto.response.product_response import ProductResponse


# ──────────────────────────────────────────────
# fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def valid_product_data():
    return {
        "name": "Bolo de Cenoura",
        "price": Decimal("45.90"),
        "category_id": uuid4(),
        "image_url": "https://example.com/bolo.jpg",
    }


# ──────────────────────────────────────────────
# ProductRequest — campo válido
# ──────────────────────────────────────────────

def test_valid_product_request(valid_product_data):
    req = ProductRequest(**valid_product_data)
    assert req.name == "Bolo de Cenoura"
    assert req.price == Decimal("45.90")
    assert req.image_url == valid_product_data["image_url"]


def test_product_request_image_url_optional(valid_product_data):
    valid_product_data.pop("image_url")
    req = ProductRequest(**valid_product_data)
    assert req.image_url is None


def test_product_request_name_strip(valid_product_data):
    valid_product_data["name"] = "  Bolo de Cenoura  "
    req = ProductRequest(**valid_product_data)
    assert req.name == "Bolo de Cenoura"


def test_product_request_price_two_decimals(valid_product_data):
    valid_product_data["price"] = Decimal("45.99")
    req = ProductRequest(**valid_product_data)
    assert req.price == Decimal("45.99")


def test_product_request_price_too_many_decimals_raises(valid_product_data):
    valid_product_data["price"] = Decimal("45.999")
    with pytest.raises(PydanticValidationError):
        ProductRequest(**valid_product_data)


# ──────────────────────────────────────────────
# ProductRequest — validações de campo
# ──────────────────────────────────────────────

@pytest.mark.parametrize("field,value,expected_msg", [
    ("name", "ab", "String should have at least 3 characters"),
    ("name", "a" * 101, "String should have at most 100 characters"),
    ("price", Decimal("0"), "greater than 0"),
    ("price", Decimal("-1"), "greater than 0"),
    ("image_url", "x" * 501, "String should have at most 500 characters"),
])
def test_product_request_field_validations(valid_product_data, field, value, expected_msg):
    data = valid_product_data.copy()
    data[field] = value
    with pytest.raises(PydanticValidationError) as exc_info:
        ProductRequest(**data)
    assert expected_msg in str(exc_info.value)


# ──────────────────────────────────────────────
# ProductResponse
# ──────────────────────────────────────────────

def test_valid_product_response():
    now = datetime.now()
    category_id = uuid4()
    resp = ProductResponse(
        id=uuid4(),
        name="Bolo de Cenoura",
        price=Decimal("45.90"),
        image_url="https://example.com/bolo.jpg",
        category_id=category_id,
        created_at=now,
        updated_at=now,
    )
    assert resp.name == "Bolo de Cenoura"
    assert resp.price == Decimal("45.90")
    assert resp.category_id == category_id


def test_product_response_image_url_optional():
    now = datetime.now()
    resp = ProductResponse(
        id=uuid4(),
        name="Bolo de Cenoura",
        price=Decimal("45.90"),
        category_id=uuid4(),
        created_at=now,
        updated_at=now,
    )
    assert resp.image_url is None
