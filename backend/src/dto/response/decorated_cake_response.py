from uuid import UUID
from datetime import datetime
from backend.src.dto.base import BaseResponse


class DecoratedCakeResponse(BaseResponse):
    id: UUID
    name: str
    slug: str
    hashtag: str
    created_at: datetime
    updated_at: datetime
