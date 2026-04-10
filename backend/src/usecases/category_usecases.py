from uuid import UUID
import logging
from backend.src.domain.models.category import Category
from backend.src.domain.repositories.category_repository import CategoryRepositoryInterface
from backend.src.dto.request.category_request import CategoryRequest
from backend.src.dto.response.category_response import CategoryResponse
from backend.src.exceptions.exception_handlers_category import (
    CategoryNotFoundException,
    CategoryNameAlreadyExistsException,
    CategorySlugAlreadyExistsException,
)

logger = logging.getLogger(__name__)


class CategoryUsecase:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    def create_category(self, category_request: CategoryRequest) -> CategoryResponse:
        if self.category_repository.get_category_by_slug(category_request.slug):
            logger.warning("Slug already exists", extra={"slug": category_request.slug})
            raise CategorySlugAlreadyExistsException(category_request.slug)

        if self.category_repository.get_category_by_name(category_request.name):
            logger.warning("Name already exists", extra={"category_name": category_request.name})
            raise CategoryNameAlreadyExistsException(category_request.name)

        category = Category(
            name=category_request.name,
            slug=category_request.slug,
            image_url=category_request.image_url,
        )
        created = self.category_repository.create_category(category)
        logger.info("Category created", extra={"category_id": created.id})
        return CategoryResponse(**created.__dict__)


    def get_category_by_id(self, category_id: UUID) -> CategoryResponse:
        category = self.category_repository.get_category_by_id(category_id)
        if not category:
            logger.warning("Category not found", extra={"category_id": category_id})
            raise CategoryNotFoundException(category_id)
        return CategoryResponse(**category.__dict__)


    def get_category_by_slug(self, slug: str) -> CategoryResponse:
        category = self.category_repository.get_category_by_slug(slug)
        if not category:
            logger.warning("Category not found", extra={"slug": slug})
            raise CategoryNotFoundException(slug=slug)
        return CategoryResponse(**category.__dict__)


    def get_all_categories(self) -> list[CategoryResponse]:
        categories = self.category_repository.get_all_categories()
        return [CategoryResponse(**category.__dict__) for category in categories]


    def update_category(self, category_id: UUID, category_request: CategoryRequest) -> CategoryResponse:
        category = self.category_repository.get_category_by_id(category_id)
        if not category:
            logger.warning("Category not found for update", extra={"category_id": category_id})
            raise CategoryNotFoundException(category_id)

        if category_request.name != category.name:
            if self.category_repository.get_category_by_name(category_request.name):
                logger.warning("Name already exists for update", extra={"category_name": category_request.name})
                raise CategoryNameAlreadyExistsException(category_request.name)


        if category_request.slug != category.slug:
            if self.category_repository.get_category_by_slug(category_request.slug):
                logger.warning("Slug already exists for update", extra={"slug": category_request.slug})
                raise CategorySlugAlreadyExistsException(category_request.slug)


        category.name = category_request.name
        category.slug = category_request.slug
        category.image_url = category_request.image_url

        updated = self.category_repository.update_category(category)
        logger.info("Category updated", extra={"category_id": updated.id})
        return CategoryResponse(**updated.__dict__)

    def delete_category(self, category_id: UUID) -> None:
        category = self.category_repository.get_category_by_id(category_id)
        if not category:
            logger.warning("Category not found for deletion", extra={"category_id": category_id})
            raise CategoryNotFoundException(category_id)

        self.category_repository.delete_category(category_id)
        logger.info("Category deleted", extra={"category_id": category_id})
