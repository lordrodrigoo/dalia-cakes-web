from uuid import UUID
import os
import logging

from fastapi import APIRouter, Depends, status

from backend.src.dto.response.instagram_post_response import InstagramPostResponse
from backend.src.dto.response.decorated_cake_response import DecoratedCakeResponse
from backend.src.usecases.instagram_usecases import InstagramPostUsecase
from backend.src.api.dependencies import get_instagram_usecase


API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
DECORATED_CAKES_PREFIX = f"{API_V1_PREFIX}/decorated-cakes"

router = APIRouter(prefix=DECORATED_CAKES_PREFIX, tags=["Decorated Cakes"])
logger = logging.getLogger(__name__)


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
