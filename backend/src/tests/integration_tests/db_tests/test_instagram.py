# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
from datetime import datetime, timezone, timedelta
import pytest
from backend.src.infra.db.entities.decorated_cake import DecoratedCakeEntity
from backend.src.infra.db.entities.instagram_post import InstagramPostEntity


# ──────────────────────────────────────────────
# DecoratedCakeEntity — CRUD direto
# ──────────────────────────────────────────────

def test_insert_decorated_cake(db_session, fake_decorated_cake):
    assert fake_decorated_cake.id is not None
    assert fake_decorated_cake.name == "Feminino"
    assert fake_decorated_cake.slug == "feminino"
    assert fake_decorated_cake.hashtag == "boloFeminino"


def test_update_decorated_cake(db_session, fake_decorated_cake):
    fake_decorated_cake.name = "Feminino Atualizado"
    db_session.commit()
    updated = db_session.query(DecoratedCakeEntity).filter_by(id=fake_decorated_cake.id).first()
    assert updated.name == "Feminino Atualizado"


def test_delete_decorated_cake(db_session, fake_decorated_cake):
    db_session.delete(fake_decorated_cake)
    db_session.commit()
    deleted = db_session.query(DecoratedCakeEntity).filter_by(id=fake_decorated_cake.id).first()
    assert deleted is None


def test_find_decorated_cake_by_id(db_session, fake_decorated_cake):
    found = db_session.query(DecoratedCakeEntity).filter_by(id=fake_decorated_cake.id).first()
    assert found is not None
    assert found.id == fake_decorated_cake.id


def test_find_all_decorated_cakes(db_session, fake_decorated_cake):
    cakes = db_session.query(DecoratedCakeEntity).all()
    assert len(cakes) >= 1


def test_decorated_cake_unique_slug_constraint(db_session, fake_decorated_cake):
    duplicate = DecoratedCakeEntity(
        name="Outro Feminino",
        slug="feminino",
        hashtag="outroHashtag",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db_session.add(duplicate)
    with pytest.raises(Exception):
        db_session.commit()


def test_decorated_cake_unique_hashtag_constraint(db_session, fake_decorated_cake):
    db_session.rollback()
    duplicate = DecoratedCakeEntity(
        name="Outro Nome",
        slug="outro-slug",
        hashtag="boloFeminino",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db_session.add(duplicate)
    with pytest.raises(Exception):
        db_session.commit()


# ──────────────────────────────────────────────
# InstagramPostEntity — CRUD direto
# ──────────────────────────────────────────────

def test_insert_instagram_post(db_session, fake_instagram_post, fake_decorated_cake):
    assert fake_instagram_post.id is not None
    assert fake_instagram_post.instagram_id == "123456789"
    assert fake_instagram_post.is_featured is True
    assert fake_instagram_post.subcategory_id == fake_decorated_cake.id


def test_update_instagram_post(db_session, fake_instagram_post):
    fake_instagram_post.is_featured = False
    db_session.commit()
    updated = db_session.query(InstagramPostEntity).filter_by(id=fake_instagram_post.id).first()
    assert updated.is_featured is False


def test_delete_instagram_post(db_session, fake_instagram_post):
    db_session.delete(fake_instagram_post)
    db_session.commit()
    deleted = db_session.query(InstagramPostEntity).filter_by(id=fake_instagram_post.id).first()
    assert deleted is None


def test_find_instagram_post_by_id(db_session, fake_instagram_post):
    found = db_session.query(InstagramPostEntity).filter_by(id=fake_instagram_post.id).first()
    assert found is not None
    assert found.instagram_id == "123456789"


def test_find_all_instagram_posts(db_session, fake_instagram_post):
    posts = db_session.query(InstagramPostEntity).all()
    assert len(posts) >= 1


def test_instagram_post_nullable_subcategory(db_session):
    now = datetime.now(timezone.utc)
    post = InstagramPostEntity(
        instagram_id="no-subcategory-001",
        caption=None,
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/ns001",
        subcategory_id=None,
        is_featured=True,
        featured_until=now + timedelta(days=3),
        synced_at=now,
        created_at=now,
        updated_at=now,
    )
    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    assert post.id is not None
    assert post.subcategory_id is None


def test_instagram_post_unique_instagram_id_constraint(db_session, fake_instagram_post):
    now = datetime.now(timezone.utc)
    duplicate = InstagramPostEntity(
        instagram_id="123456789",
        media_url="https://example.com/dup.jpg",
        permalink="https://instagram.com/p/dup",
        is_featured=False,
        featured_until=now,
        synced_at=now,
        created_at=now,
        updated_at=now,
    )
    db_session.add(duplicate)
    with pytest.raises(Exception):
        db_session.commit()
