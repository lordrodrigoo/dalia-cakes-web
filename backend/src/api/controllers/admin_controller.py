from uuid import UUID
import os
import logging

from fastapi import APIRouter, Depends, status

from backend.src.dto.request.admin_request import AdminRequest
from backend.src.dto.response.admin_response import AdminResponse
from backend.src.usecases.admin_usecases import AdminUsecase
from backend.src.api.dependencies import get_admin_usecase, get_current_user


API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
USER_PREFIX = f"{API_V1_PREFIX}/admins"

router = APIRouter(prefix=USER_PREFIX, tags=["Admins"])
logger = logging.getLogger(__name__)


@router.post("", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
def create_admin(
        admin_request: AdminRequest,
        usecase: AdminUsecase = Depends(get_admin_usecase),
        current_user: AdminResponse = Depends(get_current_user)
) -> AdminResponse:
    """Owner endpoint to create a new admin."""
    return usecase.create_admin(admin_request, current_user)


@router.get("/{admin_id}", response_model=AdminResponse)
def get_admin(
        admin_id: UUID,
        usecase: AdminUsecase = Depends(get_admin_usecase),
        _: AdminResponse = Depends(get_current_user),
) -> AdminResponse:
    """Authenticated endpoint to retrieve an admin by ID."""
    return usecase.get_admin_by_id(admin_id)


@router.put("/{admin_id}", response_model=AdminResponse)
def update_admin(
        admin_id: UUID,
        admin_request: AdminRequest,
        usecase: AdminUsecase = Depends(get_admin_usecase),
        current_user: AdminResponse = Depends(get_current_user),
) -> AdminResponse:
    """Owner or self endpoint to update an admin's data."""
    return usecase.update_admin(admin_id, admin_request, current_user)


@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(
        admin_id: UUID,
        usecase: AdminUsecase = Depends(get_admin_usecase),
        current_user: AdminResponse = Depends(get_current_user),
) -> None:
    """Owner or self endpoint to delete an admin."""
    usecase.delete_admin(admin_id, current_user)
