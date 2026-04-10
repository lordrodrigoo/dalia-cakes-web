from uuid import UUID
from datetime import datetime
from pydantic import EmailStr
from backend.src.dto.base import BaseResponse
from backend.src.domain.models.admin import AdminRole

class AdminResponse(BaseResponse):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    role: AdminRole
    created_at: datetime
    updated_at: datetime
