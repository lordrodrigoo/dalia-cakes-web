from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from backend.src.domain.models.decorated_cake import DecoratedCake


class DecoratedCakeRepositoryInterface(ABC):

    @abstractmethod
    def save(self, decorated_cake: DecoratedCake) -> DecoratedCake: pass

    @abstractmethod
    def get_by_id(self, decorated_cake_id: UUID) -> Optional[DecoratedCake]: pass

    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[DecoratedCake]: pass

    @abstractmethod
    def get_by_hashtag(self, hashtag: str) -> Optional[DecoratedCake]: pass

    @abstractmethod
    def get_all(self) -> list[DecoratedCake]: pass

    @abstractmethod
    def delete(self, decorated_cake_id: UUID) -> None: pass
