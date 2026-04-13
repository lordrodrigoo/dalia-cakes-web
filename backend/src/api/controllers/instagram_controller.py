from uuid import UUID
import os
import logging

from fastapi import APIRouter, Depends, status

from backend.src.dto.request.instagram_post_request import UpdateSubcategoryRequest
from backend.src.dto.response.instagram_post_response import InstagramPostResponse
from backend.src.usecases.instagram_usecases import InstagramPostUsecase
from backend.src.api.dependencies import get_instagram_usecase, get_current_user
from backend.src.dto.response.admin_response import AdminResponse


API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
INSTAGRAM_PREFIX = f"{API_V1_PREFIX}/instagram-posts"

router = APIRouter(prefix=INSTAGRAM_PREFIX, tags=["Instagram Posts"])
logger = logging.getLogger(__name__)


@router.get("", response_model=list[InstagramPostResponse], status_code=status.HTTP_200_OK)
def get_all_posts(
    instagram_usecase: InstagramPostUsecase = Depends(get_instagram_usecase),
):
    """Public endpoint to list all instagram posts."""
    return instagram_usecase.get_all()


@router.get("/featured", response_model=list[InstagramPostResponse], status_code=status.HTTP_200_OK)
def get_featured_posts(
    instagram_usecase: InstagramPostUsecase = Depends(get_instagram_usecase),
):
    """Public endpoint to list featured instagram posts."""
    return instagram_usecase.get_featured()


@router.get("/unclassified", response_model=list[InstagramPostResponse], status_code=status.HTTP_200_OK)
def get_unclassified_posts(
    _: AdminResponse = Depends(get_current_user),
    instagram_usecase: InstagramPostUsecase = Depends(get_instagram_usecase),
):
    """Authenticated endpoint to list posts without a subcategory."""
    return instagram_usecase.get_unclassified()


@router.patch("/{post_id}/subcategory", response_model=InstagramPostResponse, status_code=status.HTTP_200_OK)
def update_post_subcategory(
    post_id: UUID,
    request: UpdateSubcategoryRequest,
    _: AdminResponse = Depends(get_current_user),
    instagram_usecase: InstagramPostUsecase = Depends(get_instagram_usecase),
):
    """Authenticated endpoint to manually classify a post's subcategory."""
    return instagram_usecase.update_subcategory(post_id, request)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: UUID,
    _: AdminResponse = Depends(get_current_user),
    instagram_usecase: InstagramPostUsecase = Depends(get_instagram_usecase),
):
    """Authenticated endpoint to delete an instagram post."""
    instagram_usecase.delete(post_id)
