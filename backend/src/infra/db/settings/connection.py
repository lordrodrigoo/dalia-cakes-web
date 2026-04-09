#pylint: disable=redefined-outer-name
#pylint: disable=unused-import
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from backend.src.infra.db.settings.base import Base


# ENTITIES IMPORT FIX
from backend.src.infra.db.entities.user import UserEntity


load_dotenv()

class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = os.getenv("DB_URL")
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        if self.__connection_string and self.__connection_string.startswith("sqlite"):
            engine = create_engine(
                self.__connection_string,
                pool_pre_ping=True,
            )
        else:
            engine = create_engine(
                self.__connection_string,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
            )
        return engine

    def get_engine(self):
        return self.__engine

    def get_session(self):
        session_make = sessionmaker(bind=self.__engine)
        return session_make()

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
