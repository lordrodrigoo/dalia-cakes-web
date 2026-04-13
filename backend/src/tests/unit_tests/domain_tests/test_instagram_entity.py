import uuid
from datetime import datetime, timezone, timedelta
from backend.src.infra.db.entities.decorated_cake import DecoratedCakeEntity
from backend.src.infra.db.entities.instagram_post import InstagramPostEntity
from backend.src.domain.models.decorated_cake import DecoratedCake
from backend.src.domain.models.instagram_post import InstagramPost


# ──────────────────────────────────────────────
# DecoratedCakeEntity
# ──────────────────────────────────────────────

def test_decorated_cake_entity_repr():
    entity = DecoratedCakeEntity(
        id=uuid.uuid4(),
        name="Feminino",
        slug="feminino",
        hashtag="boloFeminino",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    result = repr(entity)
    assert "DecoratedCakeEntity" in result
    assert "Feminino" in result
    assert "boloFeminino" in result


# ──────────────────────────────────────────────
# DecoratedCake model
# ──────────────────────────────────────────────

def test_decorated_cake_from_entity():
    entity = DecoratedCakeEntity(
        id=uuid.uuid4(),
        name="Masculino",
        slug="masculino",
        hashtag="boloMasculino",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    model = DecoratedCake.from_entity(entity)
    assert model.id == entity.id
    assert model.name == entity.name
    assert model.slug == entity.slug
    assert model.hashtag == entity.hashtag
    assert model.created_at == entity.created_at
    assert model.updated_at == entity.updated_at


def test_decorated_cake_create():
    model = DecoratedCake.create_decorated_cake(
        name="Neutro",
        slug="neutro",
        hashtag="boloNeutro",
    )
    assert model.name == "Neutro"
    assert model.slug == "neutro"
    assert model.hashtag == "boloNeutro"
    assert model.id is None


def test_decorated_cake_repr():
    model = DecoratedCake(
        id=uuid.uuid4(),
        name="Infantil Menina",
        slug="infantil-menina",
        hashtag="boloInfantilMenina",
    )
    result = repr(model)
    assert "DecoratedCake" in result
    assert "Infantil Menina" in result
    assert "boloInfantilMenina" in result


# ──────────────────────────────────────────────
# InstagramPostEntity
# ──────────────────────────────────────────────

def test_instagram_post_entity_repr():
    now = datetime.now(timezone.utc)
    entity = InstagramPostEntity(
        id=uuid.uuid4(),
        instagram_id="123456789",
        caption="Bolo lindo #boloFeminino",
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/abc",
        is_featured=True,
        featured_until=now + timedelta(days=3),
        synced_at=now,
        created_at=now,
        updated_at=now,
    )
    result = repr(entity)
    assert "InstagramPostEntity" in result
    assert "123456789" in result


# ──────────────────────────────────────────────
# InstagramPost model
# ──────────────────────────────────────────────

def test_instagram_post_from_entity():
    now = datetime.now(timezone.utc)
    entity = InstagramPostEntity(
        id=uuid.uuid4(),
        instagram_id="987654321",
        caption="Bolo decorado #boloMasculino",
        media_url="https://example.com/img2.jpg",
        permalink="https://instagram.com/p/xyz",
        subcategory_id=None,
        is_featured=True,
        featured_until=now + timedelta(days=3),
        synced_at=now,
        created_at=now,
        updated_at=now,
    )
    model = InstagramPost.from_entity(entity)
    assert model.id == entity.id
    assert model.instagram_id == entity.instagram_id
    assert model.caption == entity.caption
    assert model.media_url == entity.media_url
    assert model.permalink == entity.permalink
    assert model.is_featured == entity.is_featured
    assert model.subcategory_id is None


def test_instagram_post_from_entity_with_subcategory():
    now = datetime.now(timezone.utc)
    subcategory_id = uuid.uuid4()
    entity = InstagramPostEntity(
        id=uuid.uuid4(),
        instagram_id="111222333",
        caption="Bolo infantil",
        media_url="https://example.com/img3.jpg",
        permalink="https://instagram.com/p/aaa",
        subcategory_id=subcategory_id,
        is_featured=False,
        featured_until=now,
        synced_at=now,
        created_at=now,
        updated_at=now,
    )
    model = InstagramPost.from_entity(entity)
    assert model.subcategory_id == subcategory_id
    assert model.is_featured is False


def test_instagram_post_repr():
    now = datetime.now(timezone.utc)
    model = InstagramPost(
        id=uuid.uuid4(),
        instagram_id="aabbcc",
        caption=None,
        media_url="https://example.com/img.jpg",
        permalink="https://instagram.com/p/aabbcc",
        is_featured=True,
        synced_at=now,
        featured_until=now + timedelta(days=3),
    )
    result = repr(model)
    assert "InstagramPost" in result
    assert "aabbcc" in result
