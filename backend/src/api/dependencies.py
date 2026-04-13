from fastapi import Depends
from fastapi.security import  HTTPAuthorizationCredentials

from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.usecases.admin_usecases import AdminUsecase
from backend.src.usecases.auth_usecases import AuthUsecase
from backend.src.dto.response.admin_response import AdminResponse
from backend.src.dto.response.token_response import TokenPayload
from backend.src.infra.db.repositories.admin_repository_interface import AdminRepository
from backend.src.usecases.category_usecases import CategoryUsecase
from backend.src.infra.db.repositories.category_repository_interface import CategoryRepository
from backend.src.usecases.product_usecases import ProductUsecase
from backend.src.infra.db.repositories.product_repository_interface import ProductRepository
from backend.src.usecases.instagram_usecases import InstagramPostUsecase
from backend.src.infra.db.repositories.instagram_post_repository_interface import InstagramPostRepository
from backend.src.infra.db.repositories.decorated_cake_repository_interface import DecoratedCakeRepository

from backend.src.config.oauth2 import oauth2_scheme
from backend.src.config.security import verify_token


def get_db():
    with DBConnectionHandler() as db:
        yield db


def get_admin_usecase(db=Depends(get_db)):
    admin_repository = AdminRepository(db)
    return AdminUsecase(admin_repository)


def get_auth_usecase(db=Depends(get_db)):
    admin_repository = AdminRepository(db)
    return AuthUsecase(admin_repository)


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
        admin_usecase: AdminUsecase = Depends(get_admin_usecase)
) -> AdminResponse:
    token_data: TokenPayload = verify_token(credentials.credentials)
    return admin_usecase.get_admin_by_id(token_data.sub)


def get_category_usecase(db=Depends(get_db)):
    category_repository = CategoryRepository(db)
    return CategoryUsecase(category_repository)


def get_product_usecase(db=Depends(get_db)):
    product_repository = ProductRepository(db)
    category_repository = CategoryRepository(db)
    return ProductUsecase(product_repository, category_repository)


def get_instagram_usecase(db=Depends(get_db)):
    instagram_post_repository = InstagramPostRepository(db)
    decorated_cake_repository = DecoratedCakeRepository(db)
    return InstagramPostUsecase(instagram_post_repository, decorated_cake_repository)
