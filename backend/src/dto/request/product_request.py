from uuid import UUID
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ProductRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    category_id: UUID = Field(...)
    image_url: Optional[str] = Field(None, max_length=500)

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value.strip()

    @field_validator('price')
    @classmethod
    def validate_price(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise ValueError("price must be greater than zero.")
        return round(value, 2)
