from uuid import UUID
from datetime import datetime
from pydantic import EmailStr
from backend.src.dto.base import BaseResponse
from backend.src.domain.models.user import UserRole

class UserResponse(BaseResponse):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    role: UserRole.ADMIN
    created_at: datetime
    updated_at: datetime
