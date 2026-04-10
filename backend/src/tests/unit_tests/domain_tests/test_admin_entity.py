import uuid
from datetime import datetime
from backend.src.infra.db.entities.admin import AdminEntity
from backend.src.domain.models.admin import Admin, AdminRole


def test_admin_entity_repr():
    entity = AdminEntity(
        id=uuid.uuid4(),
        first_name="Maria",
        last_name="Silva",
        username="maria.silva",
        email="maria@example.com",
        password="hashed",
        role=AdminRole.ADMIN.value,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    result = repr(entity)
    assert "AdminEntity" in result
    assert "maria.silva" in result
    assert "maria@example.com" in result


def test_admin_full_name():
    admin = Admin(
        first_name="Maria",
        last_name="Silva",
        username="maria.silva",
        email="maria@example.com",
        password="hashed",
        role=AdminRole.ADMIN,
    )
    assert admin.full_name == "Maria Silva"
