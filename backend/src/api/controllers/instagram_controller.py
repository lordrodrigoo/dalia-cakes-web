from uuid import UUID
import os
import logging
from typing import Optional

from fastapi import APIRouter, Depends, status
from fastapi import UploadFile, File, Form
from backend.src.usecases.upload_usecases import UploadUsecase

from backend.src.dto.request.instagram_post_request import UpdateSubcategoryRequest
from backend.src.dto.response.instagram_post_response import InstagramPostResponse
from backend.src.usecases.instagram_usecases import InstagramPostUsecase
from backend.src.api.dependencies import get_instagram_usecase, get_current_user, get_upload_usecase
from backend.src.dto.response.admin_response import AdminResponse


API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
INSTAGRAM_PREFIX = f"{API_V1_PREFIX}/instagram-posts"

router = APIRouter(prefix=INSTAGRAM_PREFIX, tags=["Instagram Posts"])
logger = logging.getLogger(__name__)



@router.post("/manual", response_model=InstagramPostResponse, status_code=status.HTTP_201_CREATED)
def create_manual_post(
    file: UploadFile = File(...),
    subcategory_id: Optional[UUID] = Form(None),
    _: AdminResponse = Depends(get_current_user),
    instagram_usecase: InstagramPostUsecase = Depends(get_instagram_usecase),
    upload_usecase: UploadUsecase = Depends(get_upload_usecase),
):
    """Authenticated endpoint to manually upload a post image."""
    file_bytes = file.file.read()
    media_url = upload_usecase.upload_image(file_bytes, "instagram", file.content_type)
    return instagram_usecase.create_manual_post(media_url, subcategory_id)



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
