# pylint: disable=unused-argument
import importlib
import os
import sys
from uuid import uuid4
from datetime import timedelta
from unittest.mock import patch, MagicMock
import pytest
from jose import jwt
from backend.src.config.owner import ensure_owner
from backend.src.config.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    SECRET_KEY,
    ALGORITHM,
)
from backend.src.exceptions.exception_handlers_auth import (
    TokenExpiredException,
    TokenInvalidException,
)


# ──────────────────────────────────────────────
# hash_password / verify_password
# ──────────────────────────────────────────────

def test_hash_password_returns_string():
    hashed = hash_password("mysecretpassword")
    assert isinstance(hashed, str)
    assert hashed != "mysecretpassword"


def test_verify_password_correct():
    hashed = hash_password("correctpassword")
    assert verify_password("correctpassword", hashed) is True


def test_verify_password_wrong():
    hashed = hash_password("correctpassword")
    assert verify_password("wrongpassword", hashed) is False


# ──────────────────────────────────────────────
# create_access_token
# ──────────────────────────────────────────────

def test_create_access_token_returns_string():
    token = create_access_token({"sub": str(uuid4()), "role": "owner"})
    assert isinstance(token, str)


def test_create_access_token_payload():
    user_id = str(uuid4())
    token = create_access_token({"sub": user_id, "role": "owner"})
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == user_id
    assert payload["role"] == "owner"


def test_create_access_token_custom_expiry():
    token = create_access_token(
        {"sub": str(uuid4()), "role": "owner"},
        expires_delta=timedelta(minutes=5),
    )
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in payload


# ──────────────────────────────────────────────
# verify_token
# ──────────────────────────────────────────────

def test_verify_token_valid():
    user_id = uuid4()
    token = create_access_token({"sub": str(user_id), "role": "owner"})
    payload = verify_token(token)
    assert payload.sub == user_id
    assert payload.role == "owner"


def test_verify_token_expired():
    token = create_access_token(
        {"sub": str(uuid4()), "role": "owner"},
        expires_delta=timedelta(seconds=-1),
    )
    with pytest.raises(TokenExpiredException):
        verify_token(token)


def test_verify_token_invalid():
    with pytest.raises(TokenInvalidException):
        verify_token("this.is.not.a.valid.token")


# ──────────────────────────────────────────────
# ensure_owner — seeder
# ──────────────────────────────────────────────

def test_seed_owner_skipped_when_env_vars_missing():
    """Seeder must do nothing when OWNER_* vars are absent (test environment)."""
    with patch.dict("os.environ", {}, clear=False):
        with patch("backend.src.config.owner.os.environ", {}):
            with patch("backend.src.config.owner.DBConnectionHandler") as mock_db:
                ensure_owner()
                mock_db.assert_not_called()


def test_seed_owner_skipped_when_owner_already_exists():
    """Seeder must not create a second owner if email already exists."""
    env = {
        "OWNER_EMAIL": "owner@test.com",
        "OWNER_USERNAME": "owner",
        "OWNER_PASSWORD": "OwnerPass@123",
    }
    with patch.dict("os.environ", env):
        mock_user_repo = MagicMock()
        mock_user_repo.get_admin_by_email.return_value = MagicMock()

        mock_db_instance = MagicMock()
        mock_db_instance.__enter__ = MagicMock(return_value=mock_db_instance)
        mock_db_instance.__exit__ = MagicMock(return_value=False)

        with patch("backend.src.config.owner.DBConnectionHandler", return_value=mock_db_instance):
            with patch("backend.src.config.owner.AdminRepository", return_value=mock_user_repo):
                ensure_owner()
                mock_user_repo.create_admin.assert_not_called()


def test_seed_owner_creates_owner_when_none_exists():
    """Seeder creates owner when no owner exists yet."""
    env = {
        "OWNER_EMAIL": "owner@test.com",
        "OWNER_USERNAME": "owner",
        "OWNER_PASSWORD": "OwnerPass@123",
    }
    with patch.dict("os.environ", env):
        mock_user_repo = MagicMock()
        mock_user_repo.get_admin_by_email.return_value = None
        mock_user_repo.get_admin_by_username.return_value = None

        mock_db_instance = MagicMock()
        mock_db_instance.__enter__ = MagicMock(return_value=mock_db_instance)
        mock_db_instance.__exit__ = MagicMock(return_value=False)

        with patch("backend.src.config.owner.DBConnectionHandler", return_value=mock_db_instance):
            with patch("backend.src.config.owner.AdminRepository", return_value=mock_user_repo):
                ensure_owner()
                mock_user_repo.create_admin.assert_called_once()


def test_seed_owner_skipped_when_username_already_taken():
    """Seeder must not proceed if username is already in use."""
    env = {
        "OWNER_EMAIL": "owner@test.com",
        "OWNER_USERNAME": "taken_username",
        "OWNER_PASSWORD": "OwnerPass@123",
    }
    with patch.dict("os.environ", env):
        mock_user_repo = MagicMock()
        mock_user_repo.get_admin_by_email.return_value = None
        mock_user_repo.get_admin_by_username.return_value = MagicMock()

        mock_db_instance = MagicMock()
        mock_db_instance.__enter__ = MagicMock(return_value=mock_db_instance)
        mock_db_instance.__exit__ = MagicMock(return_value=False)

        with patch("backend.src.config.owner.DBConnectionHandler", return_value=mock_db_instance):
            with patch("backend.src.config.owner.AdminRepository", return_value=mock_user_repo):
                ensure_owner()
                mock_user_repo.create_admin.assert_not_called()


# ──────────────────────────────────────────────
# create_refresh_token
# ──────────────────────────────────────────────

def test_create_refresh_token_returns_string():
    token = create_refresh_token({"sub": str(uuid4()), "role": "owner"})
    assert isinstance(token, str)


def test_create_refresh_token_payload():
    user_id = str(uuid4())
    token = create_refresh_token({"sub": user_id, "role": "owner"})
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == user_id
    assert payload["role"] == "owner"


def test_create_refresh_token_custom_expiry():
    token = create_refresh_token(
        {"sub": str(uuid4()), "role": "owner"},
        expires_delta=timedelta(days=1),
    )
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in payload


def test_create_refresh_token_default_expiry():
    token = create_refresh_token({"sub": str(uuid4()), "role": "owner"})
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in payload


# ──────────────────────────────────────────────
# SECRET_KEY ausente — ValueError no import
# ──────────────────────────────────────────────

def test_security_raises_value_error_when_secret_key_missing():
    """Recarrega o módulo sem SECRET_KEY e verifica o ValueError."""
    mod_name = "backend.src.config.security"
    saved_module = sys.modules.pop(mod_name)  # sempre presente antes deste teste
    original_getenv = os.getenv

    def patched_getenv(key, *args):
        if key == "SECRET_KEY":
            return None
        return original_getenv(key, *args)

    try:
        with patch("dotenv.main.load_dotenv"):
            with patch("os.getenv", side_effect=patched_getenv):
                with pytest.raises(ValueError, match="SECRET_KEY not found"):
                    importlib.import_module(mod_name)
    finally:
        sys.modules[mod_name] = saved_module  # restore simples, sem ramificação
