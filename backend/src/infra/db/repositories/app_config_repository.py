from typing import Optional
from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.infra.db.entities.app_config import AppConfigEntity


class AppConfigRepository:
    def __init__(self, db_connection: DBConnectionHandler):
        self.session = db_connection.session

    def get(self, key: str) -> Optional[str]:
        entity = self.session.query(AppConfigEntity).filter_by(key=key).first()
        return entity.value if entity else None

    def set(self, key: str, value: str) -> None:
        entity = self.session.query(AppConfigEntity).filter_by(key=key).first()
        if entity:
            entity.value = value
        else:
            self.session.add(AppConfigEntity(key=key, value=value))
        self.session.flush()
