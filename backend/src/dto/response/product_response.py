from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional
from backend.src.dto.base import BaseResponse


class ProductResponse(BaseResponse):
    id: UUID
    name: str
    price: Decimal
    image_url: Optional[str] = None
    category_id: UUID
    created_at: datetime
    updated_at: datetime
