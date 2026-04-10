import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator


SLUG_PATTERN = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


class CategoryRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    slug: str = Field(..., min_length=3, max_length=100)
    image_url: Optional[str] = Field(None, max_length=500)

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value.strip()

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, value: str) -> str:
        if not SLUG_PATTERN.match(value):
            raise ValueError("slug must be lowercase, alphanumeric and can contain hyphens.")
        return value
