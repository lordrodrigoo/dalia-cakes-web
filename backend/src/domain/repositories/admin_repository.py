from uuid import UUID
from abc import ABC, abstractmethod
from typing import Optional
from backend.src.domain.models.admin import Admin


class AdminRepositoryInterface(ABC):
    """Interface for Admin Repository - defines the contract for user data operations."""

    @abstractmethod
    def create_admin(self, user: Admin) -> Admin: pass

    @abstractmethod
    def update_admin(self, user: Admin) -> Admin: pass

    @abstractmethod
    def delete_admin(self, user_id: UUID) -> None: pass

    @abstractmethod
    def get_admin_by_id(self, user_id: UUID) -> Optional[Admin]: pass

    @abstractmethod
    def get_admin_by_email(self, email: str) -> Optional[Admin]: pass

    @abstractmethod
    def get_admin_by_username(self, username: str) -> Optional[Admin]: pass
