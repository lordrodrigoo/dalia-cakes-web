import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from backend.src.infra.db.settings.base import Base


class ProductEntity(Base):
    """Entity class representing the products table in the database."""
    __tablename__ = "products"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    image_url = Column(String(500), nullable=True)
    category_id = Column(PG_UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now, onupdate=datetime.now)

    category = relationship("CategoryEntity", back_populates="products")

    def __repr__(self):
        return f"ProductEntity(id={self.id}, name='{self.name}', price={self.price}, category_id={self.category_id})"
