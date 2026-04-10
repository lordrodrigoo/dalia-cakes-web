import os
import logging
from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.infra.db.repositories.admin_repository_interface import AdminRepository
from backend.src.domain.models.admin import Admin, AdminRole
from backend.src.config.security import hash_password



logger = logging.getLogger(__name__)

_REQUIRED_VARS = ("OWNER_EMAIL", "OWNER_USERNAME", "OWNER_PASSWORD")


def ensure_owner():
    """
    Creates the system owner on first startup if one does not exist yet.
    Requires OWNER_EMAIL, OWNER_USERNAME and OWNER_PASSWORD env vars.
    Skipped silently when those vars are absent (e.g. during tests).
    """
    missing = [var for var in _REQUIRED_VARS if var not in os.environ]
    if missing:
        logger.info(
            "Skipping owner creation: missing environment variables: %s", missing
        )
        return

    owner_email = os.environ["OWNER_EMAIL"]
    owner_username = os.environ["OWNER_USERNAME"]
    owner_password = os.environ["OWNER_PASSWORD"]
    owner_first_name = os.environ.get("OWNER_FIRST_NAME", "System")
    owner_last_name = os.environ.get("OWNER_LAST_NAME", "Owner")


    with DBConnectionHandler() as db:
        user_repo = AdminRepository(db)

        existing_owner = user_repo.get_admin_by_email(owner_email)
        if existing_owner:
            logger.info("Owner already exists — skipping creation.")
            return


        if user_repo.get_admin_by_username(owner_username):
            logger.warning("Username already exists")
            return

        user = Admin(
            email=owner_email,
            username=owner_username,
            password=hash_password(owner_password),
            first_name=owner_first_name,
            last_name=owner_last_name,
            role=AdminRole.OWNER,
        )
        user_repo.create_admin(user)
        logger.info("Owner created successfully")
