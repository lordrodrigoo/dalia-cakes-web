from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from backend.src.exceptions.custom_validation_exceptions import pydantic_validation_handler

from backend.src.exceptions.exception_handlers_admin import (
    EmailAlreadyExistsException,
    AdminNotFoundException,
    UsernameAlreadyExistsException,
    AdminPermissionDeniedException,
    email_exception_handler,
    admin_not_found_exception_handler,
    username_exception_handler,
    admin_permission_denied_exception_handler
)
from backend.src.exceptions.exception_handlers_auth import (
    TokenExpiredException,
    TokenInvalidException,
    InvalidCredentialsException,
    token_expired_exception_handler,
    token_invalid_exception_handler,
    invalid_credentials_exception_handler
)
from backend.src.exceptions.exception_handlers_category import (
    CategoryNotFoundException,
    CategoryNameAlreadyExistsException,
    CategorySlugAlreadyExistsException,
    category_not_found_exception_handler,
    category_name_already_exists_exception_handler,
    category_slug_already_exists_exception_handler
)
from backend.src.exceptions.exception_handlers_product import (
    ProductNotFoundException,
    ProductCategoryNotFoundException,
    product_not_found_exception_handler,
    product_category_not_found_exception_handler,
)
from backend.src.exceptions.exception_handlers_instagram import (
    InstagramPostNotFoundException,
    instagram_post_not_found_exception_handler,
    DecoratedCakeNotFoundException,
    decorated_cake_not_found_exception_handler
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
    app.add_exception_handler(CategoryNotFoundException, category_not_found_exception_handler)
    app.add_exception_handler(CategoryNameAlreadyExistsException, category_name_already_exists_exception_handler)
    app.add_exception_handler(CategorySlugAlreadyExistsException, category_slug_already_exists_exception_handler)
    app.add_exception_handler(ProductNotFoundException, product_not_found_exception_handler)
    app.add_exception_handler(ProductCategoryNotFoundException, product_category_not_found_exception_handler)
    app.add_exception_handler(InstagramPostNotFoundException, instagram_post_not_found_exception_handler)
    app.add_exception_handler(DecoratedCakeNotFoundException, decorated_cake_not_found_exception_handler)
