from uuid import UUID
from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class InstagramPost:
    instagram_id: str
    caption: Optional[str]
    media_url: str
    permalink: str
    is_featured: bool
    synced_at: datetime
    featured_until: datetime
    subcategory_id: Optional[UUID] = None
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_entity(cls, entity) -> "InstagramPost":
        return cls(
            id=entity.id,
            instagram_id=entity.instagram_id,
            caption=entity.caption,
            media_url=entity.media_url,
            permalink=entity.permalink,
            subcategory_id=entity.subcategory_id,
            is_featured=entity.is_featured,
            featured_until=entity.featured_until,
            synced_at=entity.synced_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def __repr__(self) -> str:
        return (
            f"InstagramPost[id={self.id}, "
            f"instagram_id={self.instagram_id}, "
            f"is_featured={self.is_featured}]"
        )
