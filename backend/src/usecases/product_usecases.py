from uuid import UUID
import logging
from backend.src.domain.models.product import Product
from backend.src.domain.repositories.product_repository import ProductRepositoryInterface
from backend.src.domain.repositories.category_repository import CategoryRepositoryInterface
from backend.src.dto.request.product_request import ProductRequest
from backend.src.dto.response.product_response import ProductResponse
from backend.src.exceptions.exception_handlers_product import (
    ProductNotFoundException,
    ProductCategoryNotFoundException,
)
from backend.src.usecases.upload_usecases import UploadUsecase

logger = logging.getLogger(__name__)


class ProductUsecase:
    def __init__(
        self,
        product_repository: ProductRepositoryInterface,
        category_repository: CategoryRepositoryInterface,
        upload_usecase: UploadUsecase = None,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository
        self.upload_usecase = upload_usecase

    def create_product(self, product_request: ProductRequest) -> ProductResponse:
        if not self.category_repository.get_category_by_id(product_request.category_id):
            logger.warning("Category not found", extra={"category_id": product_request.category_id})
            raise ProductCategoryNotFoundException(product_request.category_id)

        product = Product(
            name=product_request.name,
            price=product_request.price,
            image_url=product_request.image_url,
            category_id=product_request.category_id,
        )
        created = self.product_repository.create_product(product)
        logger.info("Product created", extra={"product_id": created.id})
        return ProductResponse(**created.__dict__)


    def get_product_by_id(self, product_id: UUID) -> ProductResponse:
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            logger.warning("Product not found", extra={"product_id": product_id})
            raise ProductNotFoundException(product_id)
        return ProductResponse(**product.__dict__)


    def get_all_products(self) -> list[ProductResponse]:
        products = self.product_repository.get_all_products()
        return [ProductResponse(**p.__dict__) for p in products]


    def get_products_by_category(self, category_id: UUID) -> list[ProductResponse]:
        if not self.category_repository.get_category_by_id(category_id):
            logger.warning("Category not found", extra={"category_id": category_id})
            raise ProductCategoryNotFoundException(category_id)

        products = self.product_repository.get_products_by_category(category_id)
        return [ProductResponse(**p.__dict__) for p in products]

    def update_product(self, product_id: UUID, product_request: ProductRequest) -> ProductResponse:
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            logger.warning("Product not found for update", extra={"product_id": product_id})
            raise ProductNotFoundException(product_id)

        if product_request.category_id != product.category_id:
            if not self.category_repository.get_category_by_id(product_request.category_id):
                logger.warning("Category not found for update", extra={"category_id": product_request.category_id})
                raise ProductCategoryNotFoundException(product_request.category_id)

        product.name = product_request.name
        product.price = product_request.price
        product.image_url = product_request.image_url
        product.category_id = product_request.category_id

        updated = self.product_repository.update_product(product)
        logger.info("Product updated", extra={"product_id": updated.id})
        return ProductResponse(**updated.__dict__)

    def delete_product(self, product_id: UUID) -> None:
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            logger.warning("Product not found for deletion", extra={"product_id": product_id})
            raise ProductNotFoundException(product_id)

        if self.upload_usecase and product.image_url:
            self.upload_usecase.delete_image(product.image_url)
        self.product_repository.delete_product(product_id)
        logger.info("Product deleted", extra={"product_id": product_id})
