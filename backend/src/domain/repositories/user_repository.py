from uuid import UUID
from abc import ABC, abstractmethod
from typing import Optional
from backend.src.domain.models.user import Users


class UserRepositoryInterface(ABC):
    """Interface for User Repository - defines the contract for user data operations."""

    @abstractmethod
    def create_user(self, user: Users) -> Users: pass

    @abstractmethod
    def update_user(self, user: Users) -> Users: pass

    @abstractmethod
    def delete_user(self, user_id: UUID) -> None: pass

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> Optional[Users]: pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[Users]: pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[Users]: pass
