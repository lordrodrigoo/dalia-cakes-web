import logging
from backend.src.domain.repositories.admin_repository import AdminRepositoryInterface
from backend.src.dto.response.token_response import TokenResponse
from backend.src.config.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    DUMMY_HASH,
)
from backend.src.exceptions.exception_handlers_auth import InvalidCredentialsException


logger = logging.getLogger(__name__)


class AuthUsecase:
    def __init__(self, admin_repository: AdminRepositoryInterface):
        self.admin_repository = admin_repository

    def login(self, username: str, password: str) -> TokenResponse:
        user = self.admin_repository.get_admin_by_username(username)

        if not user:
            verify_password(password, DUMMY_HASH)  # previne timing attack
            logger.warning("Login failed: user not found", extra={"username": username})
            raise InvalidCredentialsException()

        if not verify_password(password, user.password):
            logger.warning("Login failed: wrong password", extra={"username": username})
            raise InvalidCredentialsException()

        payload = {"sub": str(user.id), "role": user.role.value}
        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)

        logger.info("Login successful", extra={"user_id": user.id})
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    def refresh_token(self, token: str) -> TokenResponse:
        payload = verify_token(token)

        user = self.admin_repository.get_admin_by_id(payload.sub)
        if not user:
            logger.warning("Refresh failed: user not found", extra={"sub": payload.sub})
            raise InvalidCredentialsException()

        new_payload = {"sub": str(user.id), "role": user.role.value}
        new_access_token = create_access_token(new_payload)

        logger.info("Token refreshed", extra={"user_id": user.id})
        return TokenResponse(access_token=new_access_token, refresh_token=token)
