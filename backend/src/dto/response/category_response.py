from uuid import UUID
from datetime import datetime
from typing import Optional
from backend.src.dto.base import BaseResponse


class CategoryResponse(BaseResponse):
    id: UUID
    name: str
    slug: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
