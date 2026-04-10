from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from enum import Enum
from uuid import UUID


class AdminRole(Enum):
    ADMIN = "admin"
    OWNER = "owner"


@dataclass
class Admin:
    """Entity of domain - it represents an admin in the system."""
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    role: AdminRole = AdminRole.ADMIN  #default role is admin
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def full_name(self) -> str:
        """Returns the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def create_admin(
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        password: str,
        role: AdminRole = AdminRole.ADMIN
    ) -> 'Admin':
        """Factory method to create a new user."""
        return Admin(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            role=role
    )

    @staticmethod
    def from_entity(entity) -> 'Admin':
        """Converts a AdminEntity to a Users domain model."""
        return Admin(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            username=entity.username,
            email=entity.email,
            password=entity.password,
            role=AdminRole(entity.role),
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
