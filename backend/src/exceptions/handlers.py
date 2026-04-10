from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from backend.src.exceptions.custom_validation_exceptions import pydantic_validation_handler

from backend.src.exceptions.exception_handlers_admin import (
    EmailAlreadyExistsException,
    email_exception_handler,
    AdminNotFoundException,
    admin_not_found_exception_handler,
    UsernameAlreadyExistsException,
    username_exception_handler,
    AdminPermissionDeniedException,
    admin_permission_denied_exception_handler
)
from backend.src.exceptions.exception_handlers_auth import (
    TokenExpiredException,
    token_expired_exception_handler,
    TokenInvalidException,
    token_invalid_exception_handler,
    InvalidCredentialsException,
    invalid_credentials_exception_handler
)

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, pydantic_validation_handler)
    app.add_exception_handler(EmailAlreadyExistsException, email_exception_handler)
    app.add_exception_handler(AdminNotFoundException, admin_not_found_exception_handler)
    app.add_exception_handler(UsernameAlreadyExistsException, username_exception_handler)
    app.add_exception_handler(AdminPermissionDeniedException, admin_permission_denied_exception_handler)
    app.add_exception_handler(TokenExpiredException, token_expired_exception_handler)
    app.add_exception_handler(TokenInvalidException, token_invalid_exception_handler)
    app.add_exception_handler(InvalidCredentialsException, invalid_credentials_exception_handler)
