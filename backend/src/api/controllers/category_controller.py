from uuid import UUID
import os
import logging

from fastapi import APIRouter, Depends, status, Response  # Response usado apenas no POST e PUT

from backend.src.dto.request.category_request import CategoryRequest
from backend.src.dto.response.category_response import CategoryResponse
from backend.src.usecases.category_usecases import CategoryUsecase
from backend.src.api.dependencies import get_category_usecase, get_current_user
from backend.src.dto.response.admin_response import AdminResponse


API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
CATEGORY_PREFIX = f"{API_V1_PREFIX}/categories"

router = APIRouter(prefix=CATEGORY_PREFIX, tags=["Categories"])
logger = logging.getLogger(__name__)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_request: CategoryRequest,
    response: Response,
    _: AdminResponse = Depends(get_current_user),
    category_usecase: CategoryUsecase = Depends(get_category_usecase)
):

    """Authenticated endpoint to create a new category."""
    logger.info("Creating category", extra={"category_name": category_request.name})
    category = category_usecase.create_category(category_request)
    response.headers['Location'] = f"{CATEGORY_PREFIX}/{category.id}"
    return category


@router.get("", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
def get_all_categories(
    category_usecase: CategoryUsecase = Depends(get_category_usecase)
):
    """Endpoint to list all categories."""
    return category_usecase.get_all_categories()


@router.get("/slug/{slug}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_category_by_slug(
    slug: str,
    category_usecase: CategoryUsecase = Depends(get_category_usecase)
):
    """Endpoint to get a category by its slug."""
    return category_usecase.get_category_by_slug(slug)


@router.get("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_category_by_id(
    category_id: UUID,
    category_usecase: CategoryUsecase = Depends(get_category_usecase)
):
    """Endpoint to get a category by its ID."""
    return category_usecase.get_category_by_id(category_id)


@router.put("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_category(
    category_id: UUID,
    category_request: CategoryRequest,
    response: Response,
    _: AdminResponse = Depends(get_current_user),
    category_usecase: CategoryUsecase = Depends(get_category_usecase)
):
    """Authenticated endpoint to update a category."""
    logger.info("Updating category", extra={"category_id": category_id})
    updated_category = category_usecase.update_category(category_id, category_request)
    response.headers['Location'] = f"{CATEGORY_PREFIX}/{category_id}"
    return updated_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: UUID,
    _: AdminResponse = Depends(get_current_user),
    category_usecase: CategoryUsecase = Depends(get_category_usecase)
):
    """Authenticated endpoint to delete a category."""
    logger.info("Deleting category", extra={"category_id": category_id})
    category_usecase.delete_category(category_id)
