from fastapi import Depends

from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.usecases.user_usecases import UserUsecase
from backend.src.infra.db.repositories.user_repository_interface import UserRepository



def get_db():
    with DBConnectionHandler() as db:
        yield db


def get_user_usecase(db=Depends(get_db)):
    user_repository = UserRepository(db)
    return UserUsecase(user_repository)
