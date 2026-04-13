from uuid import UUID
from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class DecoratedCake:
    """"Entity of domain - it represents a decorated cake category in the system."""
    name: str
    slug: str
    hashtag: str
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_entity(cls, entity) -> "DecoratedCake":
        return cls(
            id=entity.id,
            name=entity.name,
            slug=entity.slug,
            hashtag=entity.hashtag,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def create_decorated_cake(cls, name: str, slug: str, hashtag: str) -> "DecoratedCake":
        return cls(name=name, slug=slug, hashtag=hashtag)

    def __repr__(self) -> str:
        return f"DecoratedCake[id={self.id}, name={self.name}, hashtag=#{self.hashtag}]"
