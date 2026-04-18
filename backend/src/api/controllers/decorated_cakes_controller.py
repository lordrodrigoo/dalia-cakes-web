from uuid import UUID
import os
import logging

from fastapi import APIRouter, Depends, status, Response

from backend.src.dto.request.decorated_cake_request import DecoratedCakeRequest
from backend.src.dto.response.instagram_post_response import InstagramPostResponse
from backend.src.dto.response.decorated_cake_response import DecoratedCakeResponse
from backend.src.usecases.instagram_usecases import InstagramPostUsecase
from backend.src.api.dependencies import get_instagram_usecase, get_current_user
from backend.src.dto.response.admin_response import AdminResponse

API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
DECORATED_CAKES_PREFIX = f"{API_V1_PREFIX}/decorated-cakes"

router = APIRouter(prefix=DECORATED_CAKES_PREFIX, tags=["Decorated Cakes"])
logger = logging.getLogger(__name__)


@router.post("/subcategories", response_model=DecoratedCakeResponse, status_code=status.HTTP_201_CREATED)
def create_subcategory(
    request: DecoratedCakeRequest,
    response: Response,
    _: AdminResponse = Depends(get_current_user),
    instagram_usecase: InstagramPostUsecase = Depends(get_instagram_usecase),
):
    """Authenticated endpoint to create a new decorated cake subcategory."""
    subcategory = instagram_usecase.create_subcategory(request)
    response.headers["Location"] = f"{DECORATED_CAKES_PREFIX}/subcategories/{subcategory.id}"
    return subcategory


@router.get("", response_model=list[DecoratedCakeResponse], status_code=status.HTTP_200_OK)
def get_all_subcategories(
    instagram_usecase: InstagramPostUsecase = Depends(get_instagram_usecase),
):
    """Public endpoint to list all decorated cake subcategories."""
    return instagram_usecase.get_all_subcategories()


@router.get("/{subcategory_id}/posts", response_model=list[InstagramPostResponse], status_code=status.HTTP_200_OK)
def get_posts_by_subcategory(
    subcategory_id: UUID,
    instagram_usecase: InstagramPostUsecase = Depends(get_instagram_usecase),
):
    """Public endpoint to list posts by decorated cake subcategory."""
    return instagram_usecase.get_by_subcategory(subcategory_id)


@router.put("/subcategories/{subcategory_id}", response_model=DecoratedCakeResponse, status_code=status.HTTP_200_OK)
def update_subcategory(
    subcategory_id: UUID,
    request: DecoratedCakeRequest,
    response: Response,
    _: AdminResponse = Depends(get_current_user),
    instagram_usecase: InstagramPostUsecase = Depends(get_instagram_usecase),
):
    """Authenticated endpoint to update a decorated cake subcategory."""
    updated = instagram_usecase.update_subcategory_data(subcategory_id, request)
    response.headers["Location"] = f"{DECORATED_CAKES_PREFIX}/subcategories/{subcategory_id}"
    return updated


@router.delete("/subcategories/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subcategory(
    subcategory_id: UUID,
    _: AdminResponse = Depends(get_current_user),
    instagram_usecase: InstagramPostUsecase = Depends(get_instagram_usecase),
):
    """Authenticated endpoint to delete a decorated cake subcategory."""
    instagram_usecase.delete_subcategory(subcategory_id)
