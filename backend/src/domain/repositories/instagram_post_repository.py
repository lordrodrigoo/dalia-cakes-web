from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from datetime import datetime
from backend.src.domain.models.instagram_post import InstagramPost


class InstagramPostRepositoryInterface(ABC):

    @abstractmethod
    def save(self, post: InstagramPost) -> InstagramPost: pass

    @abstractmethod
    def get_by_instagram_id(self, instagram_id: str) -> Optional[InstagramPost]: pass

    @abstractmethod
    def get_featured(self) -> list[InstagramPost]: pass

    @abstractmethod
    def get_by_subcategory(self, subcategory_id: UUID) -> list[InstagramPost]: pass

    @abstractmethod
    def get_all(self) -> list[InstagramPost]: pass

    @abstractmethod
    def get_unclassified(self) -> list[InstagramPost]: pass

    @abstractmethod
    def update_featured_status(self, post_id: UUID, is_featured: bool, featured_until: datetime) -> Optional[InstagramPost]: pass

    @abstractmethod
    def update_subcategory(self, post_id: UUID, subcategory_id: Optional[UUID]) -> InstagramPost: pass

    @abstractmethod
    def delete(self, post_id: UUID) -> None: pass
