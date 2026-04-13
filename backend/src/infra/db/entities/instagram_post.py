import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from backend.src.infra.db.settings.base import Base


class InstagramPostEntity(Base):
    __tablename__ = "instagram_posts"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instagram_id = Column(String(100), unique=True, nullable=False)
    caption = Column(String(2200), nullable=True)
    media_url = Column(String(500), nullable=False)
    permalink = Column(String(500), nullable=False)
    subcategory_id = Column(PG_UUID(as_uuid=True), ForeignKey("decorated_cakes.id"), nullable=True)
    is_featured = Column(Boolean, nullable=False, default=True)
    featured_until = Column(DateTime(timezone=True), nullable=False)
    synced_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now, onupdate=datetime.now)

    subcategory = relationship("DecoratedCakeEntity", back_populates="posts")

    def __repr__(self):
        return f"InstagramPostEntity(id={self.id}, instagram_id='{self.instagram_id}', is_featured={self.is_featured})"
