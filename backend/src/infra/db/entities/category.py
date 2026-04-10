import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from backend.src.infra.db.settings.base import Base


class CategoryEntity(Base):
    """Entity class representing the categories table in the database."""
    __tablename__ = "categories"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now, onupdate=datetime.now)

    products = relationship("ProductEntity", back_populates="category")

    def __repr__(self):
        return f"CategoryEntity(id={self.id}, name='{self.name}', slug='{self.slug}')"
