from uuid import UUID
import logging
from backend.src.domain.models.user import Users, UserRole
from backend.src.domain.repositories.user_repository import UserRepositoryInterface
from backend.src.dto.response.user_response import UserResponse
from backend.src.dto.request.user_request import UserRequest
from backend.src.domain.repositories.user_repository import UserRepositoryInterface

from backend.src.exceptions.exception_handlers_user import (
    EmailAlreadyExistsException,
    UserNotFoundException,
    UsernameAlreadyExistsException,
    UserPermissionDeniedException
)


logger = logging.getLogger(__name__)


class UserUsecase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def create_user(self, user_request: UserRequest) -> UserResponse:
        if self.user_repository.get_user_by_email(user_request.email):
            logger.warning("Email already exists", extra={"email": user_request.email})
            raise EmailAlreadyExistsException(user_request.email)

        if self.user_repository.get_user_by_username(user_request.username):
            logger.warning("Username already exists", extra={"username": user_request.username})
            raise UsernameAlreadyExistsException(user_request.username)

        user_entity = Users(
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            email=user_request.email,
            username=user_request.username,
            password=user_request.password,
            role=UserRole.ADMIN
        )
        created_user = self.user_repository.create_user(user_entity)
        logger.info("User created successfully", extra={"user_id": created_user.id})
        return UserResponse(**created_user.__dict__)

    def get_user_by_id(self, user_id: UUID) -> UserResponse:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            logger.warning("User not found", extra={"user_id": user_id})
            raise UserNotFoundException(user_id=user_id)
        return UserResponse(**user.__dict__)

    def get_user_by_email(self, email: str) -> UserResponse:
        user = self.user_repository.get_user_by_email(email)
        if not user:
            logger.warning("User not found", extra={"email": email})
            raise UserNotFoundException(email=email)
        return UserResponse(**user.__dict__)


    def update_user(
            self,
            user_id: UUID,
            user_request: UserRequest,
            current_user: UserResponse
    ) -> UserResponse:


        if current_user.id != user_id:
            logger.warning("Permission denied to update user", extra={"user_id": user_id, "requester_id": current_user.id})
            raise UserPermissionDeniedException()

        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            logger.warning("User not found for update", extra={"user_id": user_id})
            raise UserNotFoundException(user_id=user_id)


        if user_request.email and user_request.email != user.email:
            if self.user_repository.get_user_by_email(user_request.email):
                logger.warning("Email already exists for update", extra={"email": user_request.email})
                raise EmailAlreadyExistsException(user_request.email)
            user.email = user_request.email


        if user_request.username and user_request.username != user.username:
            if self.user_repository.get_user_by_username(user_request.username):
                logger.warning("Username already exists for update", extra={"username": user_request.username})
                raise UsernameAlreadyExistsException(user_request.username)
            user.username = user_request.username

        user.first_name = user_request.first_name
        user.last_name = user_request.last_name
        user.password = user_request.password

        updated_user = self.user_repository.update_user(user)
        logger.info("User updated successfully", extra={"user_id": updated_user.id})
        return UserResponse(**updated_user.__dict__)


    def delete_user(self, user_id: UUID, current_user: UserResponse) -> None:
        if current_user.id != user_id:
            logger.warning("Permission denied to delete user", extra={"user_id": user_id, "requester_id": current_user.id})
            raise UserPermissionDeniedException()

        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            logger.warning("User not found for deletion", extra={"user_id": user_id})
            raise UserNotFoundException(user_id=user_id)

        self.user_repository.delete_user(user_id)
        logger.info("User deleted successfully", extra={"user_id": user_id})
