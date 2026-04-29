# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock, patch
import pytest
from backend.src.infra.db.repositories.app_config_repository import AppConfigRepository
from backend.src.infra.db.entities.app_config import AppConfigEntity
from backend.src.infra.instagram.scheduler import refresh_token_job
from backend.src.config.settings import settings


@pytest.fixture
def session_mock():
    return MagicMock()


@pytest.fixture
def db_mock(session_mock):
    db = MagicMock()
    db.session = session_mock
    return db


@pytest.fixture
def repo(db_mock):
    return AppConfigRepository(db_mock)


def test_get_existing_key(repo, session_mock):
    entity = AppConfigEntity(key="instagram_access_token", value="my_token")
    session_mock.query.return_value.filter_by.return_value.first.return_value = entity

    result = repo.get("instagram_access_token")

    assert result == "my_token"


def test_get_missing_key_returns_none(repo, session_mock):
    session_mock.query.return_value.filter_by.return_value.first.return_value = None

    result = repo.get("nonexistent_key")

    assert result is None


def test_set_creates_new_entry(repo, session_mock):
    session_mock.query.return_value.filter_by.return_value.first.return_value = None

    repo.set("instagram_access_token", "new_token")

    session_mock.add.assert_called_once()
    session_mock.flush.assert_called_once()


def test_set_updates_existing_entry(repo, session_mock):
    entity = AppConfigEntity(key="instagram_access_token", value="old_token")
    session_mock.query.return_value.filter_by.return_value.first.return_value = entity

    repo.set("instagram_access_token", "new_token")

    assert entity.value == "new_token"
    session_mock.add.assert_not_called()
    session_mock.flush.assert_called_once()


# ──────────────────────────────────────────────
# refresh_token_job
# ──────────────────────────────────────────────

def test_refresh_token_job_success():
    with patch("backend.src.infra.instagram.scheduler.refresh_instagram_token", return_value="refreshed_token") as mock_refresh, \
         patch("backend.src.infra.instagram.scheduler.DBConnectionHandler") as mock_db, \
         patch("backend.src.infra.instagram.scheduler.AppConfigRepository") as mock_repo:

        mock_db.return_value.__enter__ = MagicMock(return_value=MagicMock())
        mock_db.return_value.__exit__ = MagicMock(return_value=False)

        refresh_token_job()

        mock_refresh.assert_called_once()
        assert settings.INSTAGRAM_ACCESS_TOKEN == "refreshed_token"
        mock_repo.return_value.set.assert_called_once_with("instagram_access_token", "refreshed_token")


def test_refresh_token_job_failure_does_not_update():
    original_token = settings.INSTAGRAM_ACCESS_TOKEN

    with patch("backend.src.infra.instagram.scheduler.refresh_instagram_token", return_value=None), \
         patch("backend.src.infra.instagram.scheduler.DBConnectionHandler"):

        refresh_token_job()

        assert settings.INSTAGRAM_ACCESS_TOKEN == original_token
