from pydantic import BaseModel
from backend.src.domain.models.user import UserRole


class RoleUpdateRequest(BaseModel):
    role: UserRole
