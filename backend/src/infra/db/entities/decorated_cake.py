import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from backend.src.infra.db.settings.base import Base


class DecoratedCakeEntity(Base):
    __tablename__ = "decorated_cakes"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    hashtag = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now, onupdate=datetime.now)

    posts = relationship("InstagramPostEntity", back_populates="subcategory")

    def __repr__(self):
        return f"DecoratedCakeEntity(id={self.id}, name='{self.name}', hashtag='#{self.hashtag}')"
