from fastapi import Depends
from fastapi.security import  HTTPAuthorizationCredentials

from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.usecases.admin_usecases import AdminUsecase
from backend.src.usecases.auth_usecases import AuthUsecase
from backend.src.dto.response.admin_response import AdminResponse
from backend.src.dto.response.token_response import TokenPayload
from backend.src.infra.db.repositories.admin_repository_interface import AdminRepository

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
