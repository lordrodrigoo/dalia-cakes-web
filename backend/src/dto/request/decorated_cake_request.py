import re
from pydantic import BaseModel, Field, field_validator

SLUG_PATTERN = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
HASHTAG_PATTERN = re.compile(r'^[a-z0-9_]+$')

class DecoratedCakeRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    slug: str = Field(..., min_length=3, max_length=100)
    hashtag: str = Field(..., min_length=2, max_length=50)

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

    @field_validator('hashtag')
    @classmethod
    def validate_hashtag(cls, value: str) -> str:
        if not HASHTAG_PATTERN.match(value):
            raise ValueError("hashtag must be lowercase, alphanumeric and can contain underscores.")
        return value.lower()
