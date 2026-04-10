from pydantic import BaseModel
from backend.src.domain.models.admin import AdminRole


class RoleUpdateRequest(BaseModel):
    role: AdminRole
