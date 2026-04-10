# pylint: disable=unused-argument
from uuid import UUID
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class EmailAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        self.message = f"Email '{email}' already exists."
        super().__init__(self.message)


async def email_exception_handler(request: Request, exc: EmailAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": exc.message}
    )


class AdminNotFoundException(Exception):
    def __init__(self, user_id: UUID = None, email: str = None):
        self.user_id = user_id
        self.email = email
        if email:
            self.message = f"User with email '{email}' not found."
        else:
            self.message = f"User with ID '{user_id}' not found."
        super().__init__(self.message)

async def admin_not_found_exception_handler(request: Request, exc: AdminNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )


class UsernameAlreadyExistsException(Exception):
    def __init__(self, username: str):
        self.username = username
        self.message = f"The username '{username}' is already registered."
        super().__init__(self.message)


async def username_exception_handler(request: Request, exc: UsernameAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=jsonable_encoder({"message": exc.message})
    )


class AdminPermissionDeniedException(Exception):
    def __init__(self):
        self.message = "You do not have permission to update this user."
        super().__init__(self.message)


async def admin_permission_denied_exception_handler(request: Request, exc: AdminPermissionDeniedException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={'message': exc.message}
    )
