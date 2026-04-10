from uuid import UUID
from typing import Optional
from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.infra.db.entities.admin import AdminEntity
from backend.src.domain.repositories.admin_repository import AdminRepositoryInterface
from backend.src.domain.models.admin import Admin, AdminRole



class AdminRepository(AdminRepositoryInterface):
    def __init__(self, db_connection: DBConnectionHandler):
        self.session = db_connection.get_session()


    def create_admin(self, user: Admin) -> Admin:
        entity = AdminEntity(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
            password=user.password,
            role=user.role.value if isinstance(user.role, AdminRole) else user.role,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.session.add(entity)
        self.session.flush()
        return Admin.from_entity(entity)

    def update_admin(self, user: Admin) -> Admin:
        entity = self.session.query(AdminEntity).filter_by(id=user.id).first()
        if entity:
            entity.first_name = user.first_name
            entity.last_name = user.last_name
            entity.email = user.email
            entity.username = user.username
            entity.password = user.password
            entity.role = user.role.value if isinstance(user.role, AdminRole) else user.role
            entity.updated_at = user.updated_at
            self.session.flush()
            return Admin.from_entity(entity)
        return None


    def get_admin_by_id(self, user_id: UUID) -> Optional[Admin]:
        entity = self.session.query(AdminEntity).filter_by(id=user_id).first()
        return Admin.from_entity(entity) if entity else None


    def delete_admin(self, user_id: UUID) -> None:
        return self.session.query(AdminEntity).filter_by(id=user_id).delete()


    def get_admin_by_email(self, email: str) -> Optional[Admin]:
        entity = self.session.query(AdminEntity).filter_by(email=email).first()
        return Admin.from_entity(entity) if entity else None


    def get_admin_by_username(self, username: str) -> Optional[Admin]:
        entity = self.session.query(AdminEntity).filter_by(username=username).first()
        return Admin.from_entity(entity) if entity else None
