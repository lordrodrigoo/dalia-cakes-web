from uuid import UUID
from pydantic import BaseModel, Field


class UpdateSubcategoryRequest(BaseModel):
    subcategory_id: UUID = Field(...)
