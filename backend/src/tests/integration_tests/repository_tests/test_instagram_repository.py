# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from backend.src.domain.models.instagram_post import InstagramPost
from backend.src.infra.db.repositories.instagram_post_repository_interface import InstagramPostRepository
from backend.src.infra.db.repositories.decorated_cake_repository_interface import DecoratedCakeRepository
from backend.src.tests.helpers import FakeDBConnectionHandler


# ──────────────────────────────────────────────
# DecoratedCakeRepository
# ──────────────────────────────────────────────

def test_get_decorated_cake_by_id(fake_decorated_cake, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = DecoratedCakeRepository(db_handler)

    result = repo.get_by_id(fake_decorated_cake.id)

    assert result is not None
    assert result.id == fake_decorated_cake.id
    assert result.name == fake_decorated_cake.name


def test_get_decorated_cake_by_id_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = DecoratedCakeRepository(db_handler)

    result = repo.get_by_id(uuid4())

    assert result is None


def test_get_decorated_cake_by_slug(fake_decorated_cake, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = DecoratedCakeRepository(db_handler)

    result = repo.get_by_slug("feminino")

    assert result is not None
    assert result.slug == "feminino"


def test_get_decorated_cake_by_slug_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = DecoratedCakeRepository(db_handler)

    result = repo.get_by_slug("nao-existe")

    assert result is None


def test_get_decorated_cake_by_hashtag(fake_decorated_cake, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = DecoratedCakeRepository(db_handler)

    result = repo.get_by_hashtag("boloFeminino")

    assert result is not None
    assert result.hashtag == "boloFeminino"


def test_get_decorated_cake_by_hashtag_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = DecoratedCakeRepository(db_handler)

    result = repo.get_by_hashtag("naoExiste")

    assert result is None


def test_get_all_decorated_cakes(fake_decorated_cake, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = DecoratedCakeRepository(db_handler)

    result = repo.get_all()

    assert len(result) >= 1
    assert any(c.name == "Feminino" for c in result)


# ──────────────────────────────────────────────
# InstagramPostRepository — save
# ──────────────────────────────────────────────

def test_save_instagram_post(fake_decorated_cake, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)
    now = datetime.now(timezone.utc)

    post = InstagramPost(
        instagram_id="999888777",
        caption="Bolo novo #boloFeminino",
        media_url="https://example.com/novo.jpg",
        permalink="https://instagram.com/p/novo",
        subcategory_id=fake_decorated_cake.id,
        is_featured=True,
        synced_at=now,
        featured_until=now + timedelta(days=3),
    )
    saved = repo.save(post)
    db_session.commit()

    assert saved.id is not None
    assert saved.instagram_id == "999888777"
    assert saved.is_featured is True


# ──────────────────────────────────────────────
# get_by_instagram_id
# ──────────────────────────────────────────────

def test_get_by_instagram_id(fake_instagram_post, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)

    result = repo.get_by_instagram_id("123456789")

    assert result is not None
    assert result.instagram_id == "123456789"


def test_get_by_instagram_id_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)

    result = repo.get_by_instagram_id("nao-existe")

    assert result is None


# ──────────────────────────────────────────────
# get_featured
# ──────────────────────────────────────────────

def test_get_featured(fake_instagram_post, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)

    result = repo.get_featured()

    assert len(result) >= 1
    assert all(p.is_featured for p in result)


# ──────────────────────────────────────────────
# get_by_subcategory
# ──────────────────────────────────────────────

def test_get_by_subcategory(fake_instagram_post, fake_decorated_cake, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)

    result = repo.get_by_subcategory(fake_decorated_cake.id)

    assert len(result) >= 1
    assert all(p.subcategory_id == fake_decorated_cake.id for p in result)


def test_get_by_subcategory_empty(db_session, fake_decorated_cake):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)

    result = repo.get_by_subcategory(uuid4())

    assert result == []


# ──────────────────────────────────────────────
# get_all
# ──────────────────────────────────────────────

def test_get_all_instagram_posts(fake_instagram_post, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)

    result = repo.get_all()

    assert len(result) >= 1


def test_get_all_instagram_posts_empty(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)

    result = repo.get_all()

    assert result == []


# ──────────────────────────────────────────────
# get_unclassified
# ──────────────────────────────────────────────

def test_get_unclassified(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)
    now = datetime.now(timezone.utc)

    post = InstagramPost(
        instagram_id="unclassified001",
        caption="Sem hashtag",
        media_url="https://example.com/sem.jpg",
        permalink="https://instagram.com/p/sem",
        subcategory_id=None,
        is_featured=True,
        synced_at=now,
        featured_until=now + timedelta(days=3),
    )
    repo.save(post)
    db_session.commit()

    result = repo.get_unclassified()

    assert len(result) >= 1
    assert all(p.subcategory_id is None for p in result)


# ──────────────────────────────────────────────
# update_featured_status
# ──────────────────────────────────────────────

def test_update_featured_status(fake_instagram_post, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)

    repo.update_featured_status(fake_instagram_post.id, False)
    db_session.commit()

    result = repo.get_by_instagram_id(fake_instagram_post.instagram_id)
    assert result.is_featured is False


# ──────────────────────────────────────────────
# update_subcategory
# ──────────────────────────────────────────────

def test_update_subcategory(fake_instagram_post, fake_decorated_cake, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)

    result = repo.update_subcategory(fake_instagram_post.id, fake_decorated_cake.id)
    db_session.commit()

    assert result.subcategory_id == fake_decorated_cake.id


def test_update_subcategory_not_found(db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)

    result = repo.update_subcategory(uuid4(), uuid4())

    assert result is None


# ──────────────────────────────────────────────
# delete
# ──────────────────────────────────────────────

def test_delete_instagram_post(fake_instagram_post, db_session):
    db_handler = FakeDBConnectionHandler(db_session)
    repo = InstagramPostRepository(db_handler)

    repo.delete(fake_instagram_post.id)
    db_session.commit()

    result = repo.get_by_instagram_id(fake_instagram_post.instagram_id)
    assert result is None
