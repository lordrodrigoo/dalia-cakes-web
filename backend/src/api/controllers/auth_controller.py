import os
import logging
from fastapi import APIRouter, status, Depends
from backend.src.dto.request.login_request import LoginRequest
from backend.src.dto.response.token_response import TokenResponse
from backend.src.dto.request.refresh_token_request import RefreshTokenRequest
from backend.src.api.dependencies import get_auth_usecase
from backend.src.usecases.auth_usecases import AuthUsecase

API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
AUTH_PREFIX = f"{API_V1_PREFIX}/auth"

router = APIRouter(prefix=AUTH_PREFIX, tags=["Auth"])
logger = logging.getLogger(__name__)

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(
    login_request: LoginRequest,
    auth_usecase: AuthUsecase = Depends(get_auth_usecase),
):
    """Public endpoint for login."""
    logger.info("Login attempt", extra={"username": login_request.username})
    return auth_usecase.login(login_request.username, login_request.password)


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def refresh_token(
    request: RefreshTokenRequest,
    auth_usecase: AuthUsecase = Depends(get_auth_usecase),
):
    """Public endpoint to refresh access token."""
    return auth_usecase.refresh_token(request.refresh_token)
