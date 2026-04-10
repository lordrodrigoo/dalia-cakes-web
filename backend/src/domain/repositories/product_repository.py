from uuid import UUID
from abc import ABC, abstractmethod
from typing import List, Optional
from backend.src.domain.models.product import Product


class ProductRepositoryInterface(ABC):
    """Interface for Product Repository - defines the contract for product data operations."""

    @abstractmethod
    def create_product(self, product: Product) -> Product: pass

    @abstractmethod
    def update_product(self, product: Product) -> Product: pass

    @abstractmethod
    def delete_product(self, product_id: UUID) -> None: pass

    @abstractmethod
    def get_product_by_id(self, product_id: UUID) -> Optional[Product]: pass

    @abstractmethod
    def get_all_products(self) -> List[Product]: pass

    @abstractmethod
    def get_products_by_category(self, category_id: UUID) -> List[Product]: pass
