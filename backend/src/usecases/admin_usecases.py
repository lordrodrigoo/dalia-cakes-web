from uuid import UUID
import logging
from backend.src.domain.models.admin import Admin, AdminRole
from backend.src.domain.repositories.admin_repository import AdminRepositoryInterface
from backend.src.dto.response.admin_response import AdminResponse
from backend.src.dto.request.admin_request import AdminRequest

from backend.src.config.security import hash_password
from backend.src.exceptions.exception_handlers_admin import (
    EmailAlreadyExistsException,
    AdminNotFoundException,
    UsernameAlreadyExistsException,
    AdminPermissionDeniedException
)


logger = logging.getLogger(__name__)


class AdminUsecase:
    def __init__(self, admin_repository: AdminRepositoryInterface):
        self.admin_repository = admin_repository

    def create_admin(
            self,
            user_request: AdminRequest,
            current_user: AdminResponse
    ) -> AdminResponse:
        if current_user.role != AdminRole.OWNER:
            logger.warning("Permission denied to create user", extra={"requester_id": current_user.id})
            raise AdminPermissionDeniedException()

        if self.admin_repository.get_admin_by_email(user_request.email):
            logger.warning("Email already exists", extra={"email": user_request.email})
            raise EmailAlreadyExistsException(user_request.email)

        if self.admin_repository.get_admin_by_username(user_request.username):
            logger.warning("Username already exists", extra={"username": user_request.username})
            raise UsernameAlreadyExistsException(user_request.username)

        user_entity = Admin(
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            email=user_request.email,
            username=user_request.username,
            password=hash_password(user_request.password),
            role=AdminRole.ADMIN
        )
        created_user = self.admin_repository.create_admin(user_entity)
        logger.info("User created successfully", extra={"user_id": created_user.id})
        return AdminResponse(**created_user.__dict__)

    def get_admin_by_id(self, user_id: UUID) -> AdminResponse:
        user = self.admin_repository.get_admin_by_id(user_id)
        if not user:
            logger.warning("User not found", extra={"user_id": user_id})
            raise AdminNotFoundException(user_id=user_id)
        return AdminResponse(**user.__dict__)

    def get_admin_by_email(self, email: str) -> AdminResponse:
        user = self.admin_repository.get_admin_by_email(email)
        if not user:
            logger.warning("User not found", extra={"email": email})
            raise AdminNotFoundException(email=email)
        return AdminResponse(**user.__dict__)


    def update_admin(
            self,
            user_id: UUID,
            user_request: AdminRequest,
            current_user: AdminResponse
    ) -> AdminResponse:


        if current_user.role != AdminRole.OWNER and current_user.id != user_id:
            logger.warning("Permission denied to update user", extra={"user_id": user_id, "requester_id": current_user.id})
            raise AdminPermissionDeniedException()

        user = self.admin_repository.get_admin_by_id(user_id)
        if not user:
            logger.warning("User not found for update", extra={"user_id": user_id})
            raise AdminNotFoundException(user_id=user_id)


        if user_request.email and user_request.email != user.email:
            if self.admin_repository.get_admin_by_email(user_request.email):
                logger.warning("Email already exists for update", extra={"email": user_request.email})
                raise EmailAlreadyExistsException(user_request.email)
            user.email = user_request.email


        if user_request.username and user_request.username != user.username:
            if self.admin_repository.get_admin_by_username(user_request.username):
                logger.warning("Username already exists for update", extra={"username": user_request.username})
                raise UsernameAlreadyExistsException(user_request.username)
            user.username = user_request.username

        user.first_name = user_request.first_name
        user.last_name = user_request.last_name
        user.password = hash_password(user_request.password)

        updated_user = self.admin_repository.update_admin(user)
        logger.info("User updated successfully", extra={"user_id": updated_user.id})
        return AdminResponse(**updated_user.__dict__)


    def delete_admin(self, user_id: UUID, current_user: AdminResponse) -> None:
        if current_user.role != AdminRole.OWNER and current_user.id != user_id:
            logger.warning("Permission denied to delete user", extra={"user_id": user_id, "requester_id": current_user.id})
            raise AdminPermissionDeniedException()

        user = self.admin_repository.get_admin_by_id(user_id)
        if not user:
            logger.warning("User not found for deletion", extra={"user_id": user_id})
            raise AdminNotFoundException(user_id=user_id)

        self.admin_repository.delete_admin(user_id)
        logger.info("User deleted successfully", extra={"user_id": user_id})
