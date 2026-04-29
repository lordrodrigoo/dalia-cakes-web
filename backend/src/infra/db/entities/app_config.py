from sqlalchemy import Column, String, Text
from backend.src.infra.db.settings.base import Base


class AppConfigEntity(Base):
    __tablename__ = "app_config"

    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=False)

    def __repr__(self):
        return f"AppConfigEntity(key='{self.key}')"
