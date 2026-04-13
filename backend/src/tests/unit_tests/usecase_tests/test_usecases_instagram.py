# pylint: disable=redefined-outer-name
from uuid import uuid4
from datetime import datetime, timezone, timedelta
import pytest
from backend.src.dto.request.instagram_post_request import UpdateSubcategoryRequest
from backend.src.exceptions.exception_handlers_instagram import (
    InstagramPostNotFoundException,
    DecoratedCakeNotFoundException,
)


# ──────────────────────────────────────────────
# sync_post — novo post
# ──────────────────────────────────────────────

def test_sync_post_new_post(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_decorated_cake_domain):
    instagram_post_repository_mock.get_by_instagram_id.return_value = None
    decorated_cake_repository_mock.get_by_hashtag.return_value = fake_decorated_cake_domain
    instagram_post_repository_mock.save.return_value = fake_instagram_post_domain

    result = instagram_usecase.sync_post(
        instagram_id="123456789",
        caption="Bolo lindo #boloFeminino",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
    )

    assert result.instagram_id == fake_instagram_post_domain.instagram_id
    instagram_post_repository_mock.save.assert_called_once()


def test_sync_post_already_exists(instagram_usecase, instagram_post_repository_mock, fake_instagram_post_domain):
    instagram_post_repository_mock.get_by_instagram_id.return_value = fake_instagram_post_domain

    result = instagram_usecase.sync_post(
        instagram_id="123456789",
        caption="Bolo lindo #boloFeminino",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
    )

    assert result.instagram_id == fake_instagram_post_domain.instagram_id
    instagram_post_repository_mock.save.assert_not_called()


def test_sync_post_no_matching_hashtag(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain):
    instagram_post_repository_mock.get_by_instagram_id.return_value = None
    decorated_cake_repository_mock.get_by_hashtag.return_value = None
    instagram_post_repository_mock.save.return_value = fake_instagram_post_domain

    result = instagram_usecase.sync_post(
        instagram_id="123456789",
        caption="Bolo lindo #semhashtagvalida",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
    )

    assert result is not None
    instagram_post_repository_mock.save.assert_called_once()


def test_sync_post_no_caption(instagram_usecase, instagram_post_repository_mock, fake_instagram_post_domain):
    instagram_post_repository_mock.get_by_instagram_id.return_value = None
    instagram_post_repository_mock.save.return_value = fake_instagram_post_domain

    result = instagram_usecase.sync_post(
        instagram_id="123456789",
        caption=None,
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
    )

    assert result is not None
    instagram_post_repository_mock.save.assert_called_once()


# ──────────────────────────────────────────────
# get_featured
# ──────────────────────────────────────────────

def test_get_featured_returns_posts(instagram_usecase, instagram_post_repository_mock, fake_instagram_post_domain):
    instagram_post_repository_mock.get_featured.return_value = [fake_instagram_post_domain]

    result = instagram_usecase.get_featured()

    assert len(result) == 1
    assert result[0].instagram_id == fake_instagram_post_domain.instagram_id


def test_get_featured_empty(instagram_usecase, instagram_post_repository_mock):
    instagram_post_repository_mock.get_featured.return_value = []

    result = instagram_usecase.get_featured()

    assert result == []


# ──────────────────────────────────────────────
# get_by_subcategory
# ──────────────────────────────────────────────

def test_get_by_subcategory_success(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_decorated_cake_domain):
    decorated_cake_repository_mock.get_by_id.return_value = fake_decorated_cake_domain
    instagram_post_repository_mock.get_by_subcategory.return_value = [fake_instagram_post_domain]

    result = instagram_usecase.get_by_subcategory(fake_decorated_cake_domain.id)

    assert len(result) == 1
    instagram_post_repository_mock.get_by_subcategory.assert_called_once_with(fake_decorated_cake_domain.id)


def test_get_by_subcategory_not_found(instagram_usecase, decorated_cake_repository_mock):
    decorated_cake_repository_mock.get_by_id.return_value = None

    with pytest.raises(DecoratedCakeNotFoundException):
        instagram_usecase.get_by_subcategory(uuid4())


# ──────────────────────────────────────────────
# get_all
# ──────────────────────────────────────────────

def test_get_all_returns_posts(instagram_usecase, instagram_post_repository_mock, fake_instagram_post_domain):
    instagram_post_repository_mock.get_all.return_value = [fake_instagram_post_domain]

    result = instagram_usecase.get_all()

    assert len(result) == 1


def test_get_all_empty(instagram_usecase, instagram_post_repository_mock):
    instagram_post_repository_mock.get_all.return_value = []

    result = instagram_usecase.get_all()

    assert result == []


# ──────────────────────────────────────────────
# get_unclassified
# ──────────────────────────────────────────────

def test_get_unclassified_returns_posts(instagram_usecase, instagram_post_repository_mock, fake_instagram_post_domain):
    instagram_post_repository_mock.get_unclassified.return_value = [fake_instagram_post_domain]

    result = instagram_usecase.get_unclassified()

    assert len(result) == 1


def test_get_unclassified_empty(instagram_usecase, instagram_post_repository_mock):
    instagram_post_repository_mock.get_unclassified.return_value = []

    result = instagram_usecase.get_unclassified()

    assert result == []


# ──────────────────────────────────────────────
# update_subcategory
# ──────────────────────────────────────────────

def test_update_subcategory_success(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_decorated_cake_domain):
    decorated_cake_repository_mock.get_by_id.return_value = fake_decorated_cake_domain
    instagram_post_repository_mock.update_subcategory.return_value = fake_instagram_post_domain

    request = UpdateSubcategoryRequest(subcategory_id=fake_decorated_cake_domain.id)
    result = instagram_usecase.update_subcategory(fake_instagram_post_domain.id, request)

    assert result.instagram_id == fake_instagram_post_domain.instagram_id
    instagram_post_repository_mock.update_subcategory.assert_called_once_with(
        fake_instagram_post_domain.id, fake_decorated_cake_domain.id
    )


def test_update_subcategory_decorated_cake_not_found(instagram_usecase, decorated_cake_repository_mock):
    decorated_cake_repository_mock.get_by_id.return_value = None

    request = UpdateSubcategoryRequest(subcategory_id=uuid4())
    with pytest.raises(DecoratedCakeNotFoundException):
        instagram_usecase.update_subcategory(uuid4(), request)


def test_update_subcategory_post_not_found(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_decorated_cake_domain):
    decorated_cake_repository_mock.get_by_id.return_value = fake_decorated_cake_domain
    instagram_post_repository_mock.update_subcategory.return_value = None

    request = UpdateSubcategoryRequest(subcategory_id=fake_decorated_cake_domain.id)
    with pytest.raises(InstagramPostNotFoundException):
        instagram_usecase.update_subcategory(uuid4(), request)


# ──────────────────────────────────────────────
# delete
# ──────────────────────────────────────────────

def test_delete_success(instagram_usecase, instagram_post_repository_mock, fake_instagram_post_domain):
    instagram_post_repository_mock.get_all.return_value = [fake_instagram_post_domain]

    instagram_usecase.delete(fake_instagram_post_domain.id)

    instagram_post_repository_mock.delete.assert_called_once_with(fake_instagram_post_domain.id)


def test_delete_not_found(instagram_usecase, instagram_post_repository_mock):
    instagram_post_repository_mock.get_all.return_value = []

    with pytest.raises(InstagramPostNotFoundException):
        instagram_usecase.delete(uuid4())


# ──────────────────────────────────────────────
# get_all_subcategories
# ──────────────────────────────────────────────

def test_get_all_subcategories(instagram_usecase, decorated_cake_repository_mock, fake_decorated_cake_domain):
    decorated_cake_repository_mock.get_all.return_value = [fake_decorated_cake_domain]

    result = instagram_usecase.get_all_subcategories()

    assert len(result) == 1
    assert result[0].name == fake_decorated_cake_domain.name


def test_get_all_subcategories_empty(instagram_usecase, decorated_cake_repository_mock):
    decorated_cake_repository_mock.get_all.return_value = []

    result = instagram_usecase.get_all_subcategories()

    assert result == []


# ──────────────────────────────────────────────
# refresh_featured_status
# ──────────────────────────────────────────────

def test_refresh_featured_status_expires_old_posts(instagram_usecase, instagram_post_repository_mock, fake_instagram_post_domain):
    now = datetime.now(timezone.utc)
    expired_post = fake_instagram_post_domain
    expired_post.is_featured = True
    expired_post.featured_until = now - timedelta(hours=1)

    instagram_post_repository_mock.get_all.return_value = [expired_post]

    instagram_usecase.refresh_featured_status()

    instagram_post_repository_mock.update_featured_status.assert_called_once_with(expired_post.id, False)


def test_refresh_featured_status_keeps_valid_posts(instagram_usecase, instagram_post_repository_mock, fake_instagram_post_domain):
    now = datetime.now(timezone.utc)
    valid_post = fake_instagram_post_domain
    valid_post.is_featured = True
    valid_post.featured_until = now + timedelta(days=2)

    instagram_post_repository_mock.get_all.return_value = [valid_post]

    instagram_usecase.refresh_featured_status()

    instagram_post_repository_mock.update_featured_status.assert_not_called()
