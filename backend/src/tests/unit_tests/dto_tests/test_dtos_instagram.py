# pylint: disable=redefined-outer-name
from uuid import uuid4
from datetime import datetime, timezone, timedelta
import pytest
from pydantic import ValidationError as PydanticValidationError
from backend.src.dto.request.instagram_post_request import UpdateSubcategoryRequest
from backend.src.dto.response.instagram_post_response import InstagramPostResponse
from backend.src.dto.response.decorated_cake_response import DecoratedCakeResponse


# ──────────────────────────────────────────────
# fixtures
# ──────────────────────────────────────────────

@pytest.fixture
def now():
    return datetime.now(timezone.utc)


@pytest.fixture
def valid_instagram_post_response_data(now):
    return {
        "id": uuid4(),
        "instagram_id": "123456789",
        "caption": "Bolo lindo #boloFeminino",
        "media_url": "https://example.com/img.jpg",
        "permalink": "https://instagram.com/p/abc",
        "subcategory_id": None,
        "is_featured": True,
        "featured_until": now + timedelta(days=3),
        "synced_at": now,
        "created_at": now,
        "updated_at": now,
    }


# ──────────────────────────────────────────────
# UpdateSubcategoryRequest
# ──────────────────────────────────────────────

def test_valid_update_subcategory_request():
    subcategory_id = uuid4()
    req = UpdateSubcategoryRequest(subcategory_id=subcategory_id)
    assert req.subcategory_id == subcategory_id


def test_update_subcategory_request_missing_field():
    with pytest.raises(PydanticValidationError):
        UpdateSubcategoryRequest()


def test_update_subcategory_request_invalid_uuid():
    with pytest.raises(PydanticValidationError):
        UpdateSubcategoryRequest(subcategory_id="not-a-uuid")


# ──────────────────────────────────────────────
# InstagramPostResponse
# ──────────────────────────────────────────────

def test_valid_instagram_post_response(valid_instagram_post_response_data):
    resp = InstagramPostResponse(**valid_instagram_post_response_data)
    assert resp.instagram_id == "123456789"
    assert resp.is_featured is True
    assert resp.subcategory_id is None


def test_instagram_post_response_caption_optional(valid_instagram_post_response_data):
    valid_instagram_post_response_data["caption"] = None
    resp = InstagramPostResponse(**valid_instagram_post_response_data)
    assert resp.caption is None


def test_instagram_post_response_with_subcategory(valid_instagram_post_response_data):
    subcategory_id = uuid4()
    valid_instagram_post_response_data["subcategory_id"] = subcategory_id
    resp = InstagramPostResponse(**valid_instagram_post_response_data)
    assert resp.subcategory_id == subcategory_id


def test_instagram_post_response_missing_required_field(valid_instagram_post_response_data):
    valid_instagram_post_response_data.pop("media_url")
    with pytest.raises(PydanticValidationError):
        InstagramPostResponse(**valid_instagram_post_response_data)


# ──────────────────────────────────────────────
# DecoratedCakeResponse
# ──────────────────────────────────────────────

def test_valid_decorated_cake_response(now):
    resp = DecoratedCakeResponse(
        id=uuid4(),
        name="Feminino",
        slug="feminino",
        hashtag="boloFeminino",
        created_at=now,
        updated_at=now,
    )
    assert resp.name == "Feminino"
    assert resp.slug == "feminino"
    assert resp.hashtag == "boloFeminino"


def test_decorated_cake_response_missing_field(now):
    with pytest.raises(PydanticValidationError):
        DecoratedCakeResponse(
            id=uuid4(),
            name="Feminino",
            slug="feminino",
            created_at=now,
            updated_at=now,
        )
