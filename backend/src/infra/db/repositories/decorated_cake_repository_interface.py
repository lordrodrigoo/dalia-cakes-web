from uuid import UUID
from typing import Optional
from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.infra.db.entities.decorated_cake import DecoratedCakeEntity
from backend.src.domain.repositories.decorated_cake_repository import DecoratedCakeRepositoryInterface
from backend.src.domain.models.decorated_cake import DecoratedCake


class DecoratedCakeRepository(DecoratedCakeRepositoryInterface):
    def __init__(self, db_connection: DBConnectionHandler):
        self.session = db_connection.get_session()

    def save(self, decorated_cake: DecoratedCake) -> DecoratedCake:
        entity = self.session.query(DecoratedCakeEntity).filter_by(id=decorated_cake.id).first()
        if entity:
            entity.name = decorated_cake.name
            entity.slug = decorated_cake.slug
            entity.hashtag = decorated_cake.hashtag
        else:
            entity = DecoratedCakeEntity(
                name=decorated_cake.name,
                slug=decorated_cake.slug,
                hashtag=decorated_cake.hashtag,
            )
            self.session.add(entity)
        self.session.flush()
        return DecoratedCake.from_entity(entity)

    def get_by_id(self, decorated_cake_id: UUID) -> Optional[DecoratedCake]:
        entity = self.session.query(DecoratedCakeEntity).filter_by(id=decorated_cake_id).first()
        return DecoratedCake.from_entity(entity) if entity else None

    def get_by_slug(self, slug: str) -> Optional[DecoratedCake]:
        entity = self.session.query(DecoratedCakeEntity).filter_by(slug=slug).first()
        return DecoratedCake.from_entity(entity) if entity else None

    def get_by_hashtag(self, hashtag: str) -> Optional[DecoratedCake]:
        entity = self.session.query(DecoratedCakeEntity).filter_by(hashtag=hashtag).first()
        return DecoratedCake.from_entity(entity) if entity else None

    def get_all(self) -> list[DecoratedCake]:
        entities = self.session.query(DecoratedCakeEntity).all()
        return [DecoratedCake.from_entity(e) for e in entities]

    def delete(self, decorated_cake_id: UUID) -> None:
        self.session.query(DecoratedCakeEntity).filter_by(id=decorated_cake_id).delete()
