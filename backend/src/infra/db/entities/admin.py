import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from backend.src.infra.db.settings.base import Base

from backend.src.domain.models.admin import AdminRole


class AdminEntity(Base):
    """Entity class representing the users table in the database."""
    __tablename__ = "users"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)
    username = Column(String(25), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default=AdminRole.ADMIN.value)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now, onupdate=datetime.now)


    def __repr__(self):
        return (
            f"AdminEntity(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', "
            f"username='{self.username}', email='{self.email}', role='{self.role}')"
        )
