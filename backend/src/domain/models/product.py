from uuid import UUID
from datetime import datetime
from typing import Optional
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class Product:
    """Entity of domain - it represents a product in the system."""
    name: str
    price: Decimal
    category_id: UUID
    image_url: Optional[str] = None
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def full_description(self) -> str:
        return f"{self.name} - ${self.price:.2f}"

    @classmethod
    def create_product(
        cls,
        name: str,
        image_url: Optional[str],
        price: Decimal,
        category_id: UUID
    ) -> "Product":
        return cls(name=name, image_url=image_url, price=price, category_id=category_id)

    @staticmethod
    def from_entity(entity) -> "Product":
        return Product(
            id=entity.id,
            name=entity.name,
            price=entity.price,
            image_url=entity.image_url,
            category_id=entity.category_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def __repr__(self) -> str:
        return f"Product[id={self.id}, name={self.name}, price={self.price}]"
