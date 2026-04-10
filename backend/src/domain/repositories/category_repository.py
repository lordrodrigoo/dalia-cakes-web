from uuid import UUID
from typing import Optional, List
from abc import ABC, abstractmethod
from backend.src.domain.models.category import Category


class CategoryRepositoryInterface(ABC):
    """Interface for Category Repository - defines the contract for category data operations."""

    @abstractmethod
    def create_category(self, category: Category) -> Category: pass

    @abstractmethod
    def update_category(self, category: Category) -> Category: pass

    @abstractmethod
    def delete_category(self, category_id: UUID) -> None: pass

    @abstractmethod
    def get_category_by_id(self, category_id: UUID) -> Optional[Category]: pass

    @abstractmethod
    def get_category_by_slug(self, slug: str) -> Optional[Category]: pass

    @abstractmethod
    def get_all_categories(self) -> List[Category]: pass

    @abstractmethod
    def get_category_by_name(self, name: str) -> Optional[Category]: pass
