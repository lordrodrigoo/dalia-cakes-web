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
    decorated_cake_repository_mock.get_all.return_value = [fake_decorated_cake_domain]
    instagram_post_repository_mock.save.return_value = fake_instagram_post_domain

    result = instagram_usecase.sync_post(
        instagram_id="123456789",
        caption="Bolo lindo #feminino",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
    )

    assert result.instagram_id == fake_instagram_post_domain.instagram_id
    instagram_post_repository_mock.save.assert_called_once()


def test_sync_post_already_exists(instagram_usecase, instagram_post_repository_mock, fake_instagram_post_domain):
    # fake_instagram_post_domain já tem subcategory_id — deve retornar sem reclassificar
    instagram_post_repository_mock.get_by_instagram_id.return_value = fake_instagram_post_domain

    result = instagram_usecase.sync_post(
        instagram_id="123456789",
        caption="Bolo lindo #feminino",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
    )

    assert result.instagram_id == fake_instagram_post_domain.instagram_id
    instagram_post_repository_mock.save.assert_not_called()
    instagram_post_repository_mock.update_subcategory.assert_not_called()


def test_sync_post_no_matching_hashtag(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_decorated_cake_domain):
    # Sem "outros" nas subcategorias — deve salvar sem subcategory_id
    instagram_post_repository_mock.get_by_instagram_id.return_value = None
    decorated_cake_repository_mock.get_all.return_value = [fake_decorated_cake_domain]
    instagram_post_repository_mock.save.return_value = fake_instagram_post_domain

    result = instagram_usecase.sync_post(
        instagram_id="123456789",
        caption="Bolo lindo sem categoria",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
    )

    assert result is not None
    save_call = instagram_post_repository_mock.save.call_args[0][0]
    assert save_call.subcategory_id is None


def test_sync_post_no_caption(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain):
    instagram_post_repository_mock.get_by_instagram_id.return_value = None
    decorated_cake_repository_mock.get_all.return_value = []
    instagram_post_repository_mock.save.return_value = fake_instagram_post_domain

    result = instagram_usecase.sync_post(
        instagram_id="123456789",
        caption=None,
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
    )

    assert result is not None
    instagram_post_repository_mock.save.assert_called_once()


def test_sync_post_hashtag_contains_match(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_decorated_cake_domain):
    """boloFeminino deve casar com subcategoria cujo hashtag é 'feminino'."""
    instagram_post_repository_mock.get_by_instagram_id.return_value = None
    decorated_cake_repository_mock.get_all.return_value = [fake_decorated_cake_domain]
    instagram_post_repository_mock.save.return_value = fake_instagram_post_domain

    instagram_usecase.sync_post(
        instagram_id="abc",
        caption="#boloFeminino lindo",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
    )

    save_call = instagram_post_repository_mock.save.call_args[0][0]
    assert save_call.subcategory_id == fake_decorated_cake_domain.id


def test_sync_post_plain_word_match(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_decorated_cake_domain):
    """Palavra sem # no caption também deve classificar o post."""
    instagram_post_repository_mock.get_by_instagram_id.return_value = None
    decorated_cake_repository_mock.get_all.return_value = [fake_decorated_cake_domain]
    instagram_post_repository_mock.save.return_value = fake_instagram_post_domain

    instagram_usecase.sync_post(
        instagram_id="xyz",
        caption="Bolo feminino para aniversario",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/xyz",
    )

    save_call = instagram_post_repository_mock.save.call_args[0][0]
    assert save_call.subcategory_id == fake_decorated_cake_domain.id


def test_sync_post_case_insensitive_match(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_decorated_cake_domain):
    """Correspondência deve ser insensível a maiúsculas/minúsculas."""
    instagram_post_repository_mock.get_by_instagram_id.return_value = None
    decorated_cake_repository_mock.get_all.return_value = [fake_decorated_cake_domain]
    instagram_post_repository_mock.save.return_value = fake_instagram_post_domain

    instagram_usecase.sync_post(
        instagram_id="zzz",
        caption="#BOLOFEMININO",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/zzz",
    )

    save_call = instagram_post_repository_mock.save.call_args[0][0]
    assert save_call.subcategory_id == fake_decorated_cake_domain.id


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

    call_args = instagram_post_repository_mock.update_featured_status.call_args
    assert call_args[0][0] == expired_post.id
    assert call_args[0][1] is False


def test_refresh_featured_status_keeps_valid_posts(instagram_usecase, instagram_post_repository_mock, fake_instagram_post_domain):
    now = datetime.now(timezone.utc)
    valid_post = fake_instagram_post_domain
    valid_post.is_featured = True
    valid_post.featured_until = now + timedelta(days=2)

    instagram_post_repository_mock.get_all.return_value = [valid_post]

    instagram_usecase.refresh_featured_status()

    instagram_post_repository_mock.update_featured_status.assert_not_called()


# ──────────────────────────────────────────────
# _classify_post — catch-all Outros
# ──────────────────────────────────────────────

def test_classify_post_falls_back_to_outros(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_decorated_cake_domain, fake_outros_cake_domain):
    """Sem match de hashtag específico, deve atribuir a categoria Outros."""
    instagram_post_repository_mock.get_by_instagram_id.return_value = None
    decorated_cake_repository_mock.get_all.return_value = [fake_decorated_cake_domain, fake_outros_cake_domain]
    instagram_post_repository_mock.save.return_value = fake_instagram_post_domain

    instagram_usecase.sync_post(
        instagram_id="no_match",
        caption="Caixinha de doces especial",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/no_match",
    )

    save_call = instagram_post_repository_mock.save.call_args[0][0]
    assert save_call.subcategory_id == fake_outros_cake_domain.id


def test_classify_post_no_caption_falls_back_to_outros(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_outros_cake_domain):
    """Post sem caption deve ir para Outros."""
    instagram_post_repository_mock.get_by_instagram_id.return_value = None
    decorated_cake_repository_mock.get_all.return_value = [fake_outros_cake_domain]
    instagram_post_repository_mock.save.return_value = fake_instagram_post_domain

    instagram_usecase.sync_post(
        instagram_id="no_caption",
        caption=None,
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/no_caption",
    )

    save_call = instagram_post_repository_mock.save.call_args[0][0]
    assert save_call.subcategory_id == fake_outros_cake_domain.id


def test_classify_post_outros_slug_not_matched_as_specific(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_decorated_cake_domain, fake_outros_cake_domain):
    """Categoria Outros deve ser ignorada no matching específico e usada só como fallback."""
    instagram_post_repository_mock.get_by_instagram_id.return_value = None
    decorated_cake_repository_mock.get_all.return_value = [fake_outros_cake_domain, fake_decorated_cake_domain]
    instagram_post_repository_mock.save.return_value = fake_instagram_post_domain

    instagram_usecase.sync_post(
        instagram_id="feminino_post",
        caption="Bolo feminino lindo",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/fem",
    )

    save_call = instagram_post_repository_mock.save.call_args[0][0]
    assert save_call.subcategory_id == fake_decorated_cake_domain.id


# ──────────────────────────────────────────────
# sync_post — reclassificação de post existente sem subcategoria
# ──────────────────────────────────────────────

def test_sync_post_existing_refreshes_media_url(instagram_usecase, instagram_post_repository_mock, fake_instagram_post_domain):
    """URL é sempre atualizada para posts existentes, mesmo já classificados."""
    instagram_post_repository_mock.get_by_instagram_id.return_value = fake_instagram_post_domain

    instagram_usecase.sync_post(
        instagram_id=fake_instagram_post_domain.instagram_id,
        caption="caption",
        media_url="https://new-cdn.instagram.com/fresh.jpg",
        permalink="https://instagram.com/p/abc",
    )

    instagram_post_repository_mock.refresh_media_url.assert_called_once_with(
        fake_instagram_post_domain.id,
        "https://new-cdn.instagram.com/fresh.jpg",
        "https://instagram.com/p/abc",
    )


def test_sync_post_existing_unclassified_gets_reclassified(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_decorated_cake_domain):
    """Post existente sem subcategoria deve ser reclassificado ao sincronizar."""
    unclassified_post = fake_instagram_post_domain
    unclassified_post.subcategory_id = None

    instagram_post_repository_mock.get_by_instagram_id.return_value = unclassified_post
    decorated_cake_repository_mock.get_all.return_value = [fake_decorated_cake_domain]
    instagram_post_repository_mock.update_subcategory.return_value = fake_instagram_post_domain

    instagram_usecase.sync_post(
        instagram_id=unclassified_post.instagram_id,
        caption="Bolo feminino especial",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
    )

    instagram_post_repository_mock.update_subcategory.assert_called_once_with(
        unclassified_post.id, fake_decorated_cake_domain.id
    )
    instagram_post_repository_mock.save.assert_not_called()


def test_sync_post_existing_unclassified_no_match_stays_unclassified(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_decorated_cake_domain):
    """Post existente sem subcategoria e sem match deve permanecer sem subcategoria."""
    unclassified_post = fake_instagram_post_domain
    unclassified_post.subcategory_id = None

    instagram_post_repository_mock.get_by_instagram_id.return_value = unclassified_post
    decorated_cake_repository_mock.get_all.return_value = [fake_decorated_cake_domain]

    instagram_usecase.sync_post(
        instagram_id=unclassified_post.instagram_id,
        caption="Post sem hashtag relevante",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
    )

    instagram_post_repository_mock.update_subcategory.assert_not_called()
    instagram_post_repository_mock.save.assert_not_called()


# ──────────────────────────────────────────────
# reclassify_unclassified_posts
# ──────────────────────────────────────────────

def test_reclassify_unclassified_posts_classifies_all(instagram_usecase, instagram_post_repository_mock, decorated_cake_repository_mock, fake_instagram_post_domain, fake_decorated_cake_domain):
    unclassified = fake_instagram_post_domain
    unclassified.subcategory_id = None
    unclassified.caption = "Bolo feminino"

    instagram_post_repository_mock.get_unclassified.return_value = [unclassified]
    decorated_cake_repository_mock.get_all.return_value = [fake_decorated_cake_domain]

    count = instagram_usecase.reclassify_unclassified_posts()

    assert count == 1
    instagram_post_repository_mock.update_subcategory.assert_called_once_with(
        unclassified.id, fake_decorated_cake_domain.id
    )


def test_reclassify_unclassified_posts_empty(instagram_usecase, instagram_post_repository_mock):
    instagram_post_repository_mock.get_unclassified.return_value = []

    count = instagram_usecase.reclassify_unclassified_posts()

    assert count == 0
    instagram_post_repository_mock.update_subcategory.assert_not_called()
