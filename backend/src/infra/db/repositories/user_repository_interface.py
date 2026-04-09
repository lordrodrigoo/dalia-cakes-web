from uuid import UUID
from typing import Optional
from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.infra.db.entities.user import UserEntity
from backend.src.domain.repositories.user_repository import UserRepositoryInterface
from backend.src.domain.models.user import Users, UserRole



class UserRepository(UserRepositoryInterface):
    def __init__(self, db_connection: DBConnectionHandler):
        self.session = db_connection.get_session()


    def create_user(self, user: Users) -> Users:
        entity = UserEntity(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
            password=user.password,
            role=user.role.value if isinstance(user.role, UserRole) else user.role,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.session.add(entity)
        self.session.flush()
        return Users.from_entity(entity)

    def update_user(self, user: Users) -> Users:
        entity = self.session.query(UserEntity).filter_by(id=user.id).first()
        if entity:
            entity.first_name = user.first_name
            entity.last_name = user.last_name
            entity.email = user.email
            entity.username = user.username
            entity.password = user.password
            entity.role = user.role.value if isinstance(user.role, UserRole) else user.role
            entity.updated_at = user.updated_at
            self.session.flush()
            return Users.from_entity(entity)
        return None


    def get_user_by_id(self, user_id: UUID) -> Optional[Users]:
        entity = self.session.query(UserEntity).filter_by(id=user_id).first()
        return Users.from_entity(entity) if entity else None


    def delete_user(self, user_id: UUID) -> None:
        return self.session.query(UserEntity).filter_by(id=user_id).delete()


    def get_user_by_email(self, email: str) -> Optional[Users]:
        entity = self.session.query(UserEntity).filter_by(email=email).first()
        return Users.from_entity(entity) if entity else None


    def get_user_by_username(self, username: str) -> Optional[Users]:
        entity = self.session.query(UserEntity).filter_by(username=username).first()
        return Users.from_entity(entity) if entity else None
