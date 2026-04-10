from uuid import UUID
from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class Category:
    """Entity of domain - it represents a category in the system."""
    name: str
    slug: str
    image_url: Optional[str] = None
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create_category(
        cls,
        name: str,
        slug: str,
        image_url: Optional[str] = None
    ) -> "Category":
        return cls(name=name, slug=slug, image_url=image_url)

    @classmethod
    def from_entity(cls, entity) -> "Category":
        return cls(
            id=entity.id,
            name=entity.name,
            slug=entity.slug,
            image_url=entity.image_url,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def __repr__(self) -> str:
        return f"Category[id={self.id}, name={self.name}, slug={self.slug}]"
