import os
import logging
from fastapi import APIRouter, Depends, UploadFile, File, Query, status

from backend.src.usecases.upload_usecases import UploadUsecase
from backend.src.dto.response.upload_response import UploadResponse
from backend.src.api.dependencies import get_upload_usecase, get_current_user
from backend.src.dto.response.admin_response import AdminResponse

API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")

router = APIRouter(prefix=f"{API_V1_PREFIX}/upload", tags=["Upload"])
logger = logging.getLogger(__name__)


@router.post("/image", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
def upload_image(
    file: UploadFile = File(...),
    folder: str = Query(default="products"),
    _: AdminResponse = Depends(get_current_user),
    upload_usecase: UploadUsecase = Depends(get_upload_usecase),
):
    """Authenticated endpoint to upload and process an image to S3."""
    file_bytes = file.file.read()
    url = upload_usecase.upload_image(file_bytes, folder, file.content_type)
    logger.info("Image uploaded", extra={"folder": folder})
    return UploadResponse(url=url)
