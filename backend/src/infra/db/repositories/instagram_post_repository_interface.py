from uuid import UUID
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import and_, desc
from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.infra.db.entities.instagram_post import InstagramPostEntity
from backend.src.domain.repositories.instagram_post_repository import InstagramPostRepositoryInterface
from backend.src.domain.models.instagram_post import InstagramPost



class InstagramPostRepository(InstagramPostRepositoryInterface):
    def __init__(self, db_connection: DBConnectionHandler):
        self.session = db_connection.session

    def save(self, post: InstagramPost) -> InstagramPost:
        entity = InstagramPostEntity(
            instagram_id=post.instagram_id,
            caption=post.caption,
            media_url=post.media_url,
            permalink=post.permalink,
            subcategory_id=post.subcategory_id,
            is_featured=post.is_featured,
            featured_until=post.featured_until,
            synced_at=post.synced_at,
        )
        self.session.add(entity)
        self.session.flush()
        return InstagramPost.from_entity(entity)

    def get_by_instagram_id(self, instagram_id: str) -> Optional[InstagramPost]:
        entity = self.session.query(InstagramPostEntity).filter_by(instagram_id=instagram_id).first()
        return InstagramPost.from_entity(entity) if entity else None

    FEATURED_FALLBACK_LIMIT = 12

    def get_featured(self) -> list[InstagramPost]:
        now = datetime.now(timezone.utc)
        entities = self.session.query(InstagramPostEntity).filter(
            and_(
                InstagramPostEntity.is_featured.is_(True),
                InstagramPostEntity.featured_until >= now,
            )
        ).all()
        if entities:
            return [InstagramPost.from_entity(e) for e in entities]
        # Fallback: nenhum post featured ativo — retorna os mais recentes
        fallback = (
            self.session.query(InstagramPostEntity)
            .order_by(desc(InstagramPostEntity.synced_at))
            .limit(self.FEATURED_FALLBACK_LIMIT)
            .all()
        )
        return [InstagramPost.from_entity(e) for e in fallback]

    def get_by_subcategory(self, subcategory_id: UUID) -> list[InstagramPost]:
        entities = self.session.query(InstagramPostEntity).filter_by(subcategory_id=subcategory_id).all()
        return [InstagramPost.from_entity(e) for e in entities]

    def get_all(self) -> list[InstagramPost]:
        entities = self.session.query(InstagramPostEntity).all()
        return [InstagramPost.from_entity(e) for e in entities]

    def get_unclassified(self) -> list[InstagramPost]:
        entities = self.session.query(InstagramPostEntity).filter(
            InstagramPostEntity.subcategory_id.is_(None)
        ).all()
        return [InstagramPost.from_entity(e) for e in entities]

    def update_featured_status(self, post_id: UUID, is_featured: bool, featured_until: datetime) -> Optional[InstagramPost]:
        entity = self.session.query(InstagramPostEntity).filter_by(id=post_id).first()
        if entity:
            entity.is_featured = is_featured
            entity.featured_until = featured_until
            self.session.flush()
            return InstagramPost.from_entity(entity)
        return None

    def update_subcategory(self, post_id: UUID, subcategory_id: Optional[UUID]) -> InstagramPost:
        entity = self.session.query(InstagramPostEntity).filter_by(id=post_id).first()
        if entity:
            entity.subcategory_id = subcategory_id
            self.session.flush()
            return InstagramPost.from_entity(entity)
        return None

    def delete(self, post_id: UUID) -> None:
        self.session.query(InstagramPostEntity).filter_by(id=post_id).delete()
