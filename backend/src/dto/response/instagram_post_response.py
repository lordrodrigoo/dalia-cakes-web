from uuid import UUID
from datetime import datetime
from typing import Optional
from backend.src.dto.base import BaseResponse


class InstagramPostResponse(BaseResponse):
    id: UUID
    instagram_id: str
    caption: Optional[str] = None
    media_url: str
    permalink: str
    subcategory_id: Optional[UUID] = None
    is_featured: bool
    featured_until: datetime
    synced_at: datetime
    created_at: datetime
    updated_at: datetime
