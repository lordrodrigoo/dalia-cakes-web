# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
from uuid import uuid4
from unittest.mock import MagicMock
import pytest
from backend.src.dto.request.user_request import UserRequest
from backend.src.exceptions.exception_handlers_user import (
    EmailAlreadyExistsException,
    UserNotFoundException,
    UsernameAlreadyExistsException,
    UserPermissionDeniedException,
)


# ──────────────────────────────────────────────
# create_user
# ──────────────────────────────────────────────

def test_create_user_success(usecase, user_repository_mock, valid_user_data, fake_user_domain):
    user_repository_mock.get_user_by_email.return_value = None
    user_repository_mock.get_user_by_username.return_value = None
    user_repository_mock.create_user.return_value = fake_user_domain

    request = UserRequest(**valid_user_data)
    result = usecase.create_user(request)

    assert result.email == valid_user_data["email"]
    assert result.username == valid_user_data["username"]
    user_repository_mock.create_user.assert_called_once()


def test_create_user_email_already_exists(usecase, user_repository_mock, valid_user_data, fake_user_domain):
    user_repository_mock.get_user_by_email.return_value = fake_user_domain

    request = UserRequest(**valid_user_data)
    with pytest.raises(EmailAlreadyExistsException) as exc_info:
        usecase.create_user(request)

    assert valid_user_data["email"] in exc_info.value.message


def test_create_user_username_already_exists(usecase, user_repository_mock, valid_user_data, fake_user_domain):
    user_repository_mock.get_user_by_email.return_value = None
    user_repository_mock.get_user_by_username.return_value = fake_user_domain

    request = UserRequest(**valid_user_data)
    with pytest.raises(UsernameAlreadyExistsException) as exc_info:
        usecase.create_user(request)

    assert valid_user_data["username"] in exc_info.value.message


# ──────────────────────────────────────────────
# get_user_by_id
# ──────────────────────────────────────────────

def test_get_user_by_id_success(usecase, user_repository_mock, fake_user_domain):
    user_repository_mock.get_user_by_id.return_value = fake_user_domain

    result = usecase.get_user_by_id(fake_user_domain.id)

    assert result.id == fake_user_domain.id
    user_repository_mock.get_user_by_id.assert_called_once_with(fake_user_domain.id)


def test_get_user_by_id_not_found(usecase, user_repository_mock):
    user_repository_mock.get_user_by_id.return_value = None

    with pytest.raises(UserNotFoundException):
        usecase.get_user_by_id("non-existent-id")


# ──────────────────────────────────────────────
# get_user_by_email
# ──────────────────────────────────────────────

def test_get_user_by_email_success(usecase, user_repository_mock, fake_user_domain):
    user_repository_mock.get_user_by_email.return_value = fake_user_domain

    result = usecase.get_user_by_email(fake_user_domain.email)

    assert result.email == fake_user_domain.email


def test_get_user_by_email_not_found(usecase, user_repository_mock):
    user_repository_mock.get_user_by_email.return_value = None

    with pytest.raises(UserNotFoundException) as exc_info:
        usecase.get_user_by_email("notfound@example.com")

    assert "notfound@example.com" in exc_info.value.message


# ──────────────────────────────────────────────
# update_user
# ──────────────────────────────────────────────

def test_update_user_success(usecase, user_repository_mock, valid_user_data, fake_user_domain, current_user):
    user_repository_mock.get_user_by_id.return_value = fake_user_domain
    user_repository_mock.get_user_by_email.return_value = None
    user_repository_mock.get_user_by_username.return_value = None
    user_repository_mock.update_user.return_value = fake_user_domain

    request = UserRequest(**valid_user_data)
    result = usecase.update_user(current_user.id, request, current_user)

    assert result.id == fake_user_domain.id
    user_repository_mock.update_user.assert_called_once()


def test_update_user_permission_denied(usecase, user_repository_mock, valid_user_data, current_user):
    other_id = uuid4()

    request = UserRequest(**valid_user_data)
    with pytest.raises(UserPermissionDeniedException):
        usecase.update_user(other_id, request, current_user)


def test_update_user_not_found(usecase, user_repository_mock, valid_user_data, current_user):
    user_repository_mock.get_user_by_id.return_value = None

    request = UserRequest(**valid_user_data)
    with pytest.raises(UserNotFoundException):
        usecase.update_user(current_user.id, request, current_user)


def test_update_user_email_conflict(usecase, user_repository_mock, valid_user_data, fake_user_domain, current_user):
    other_user = MagicMock()
    other_user.email = "other@example.com"

    fake_user_domain.email = "old@example.com"
    valid_user_data["email"] = "new@example.com"
    valid_user_data["email"] = "new@example.com"

    user_repository_mock.get_user_by_id.return_value = fake_user_domain
    user_repository_mock.get_user_by_email.return_value = other_user

    request = UserRequest(**valid_user_data)
    with pytest.raises(EmailAlreadyExistsException):
        usecase.update_user(current_user.id, request, current_user)


def test_update_user_username_conflict(usecase, user_repository_mock, valid_user_data, fake_user_domain, current_user):
    other_user = MagicMock()
    other_user.username = "other.user"

    fake_user_domain.username = "old.username"
    valid_user_data["username"] = "new.username"

    user_repository_mock.get_user_by_id.return_value = fake_user_domain
    user_repository_mock.get_user_by_email.return_value = None
    user_repository_mock.get_user_by_username.return_value = other_user

    request = UserRequest(**valid_user_data)
    with pytest.raises(UsernameAlreadyExistsException):
        usecase.update_user(current_user.id, request, current_user)


# ──────────────────────────────────────────────
# delete_user
# ──────────────────────────────────────────────

def test_delete_user_success(usecase, user_repository_mock, fake_user_domain, current_user):
    user_repository_mock.get_user_by_id.return_value = fake_user_domain

    usecase.delete_user(current_user.id, current_user)

    user_repository_mock.delete_user.assert_called_once_with(current_user.id)


def test_delete_user_permission_denied(usecase, user_repository_mock, current_user):
    other_id = uuid4()

    with pytest.raises(UserPermissionDeniedException):
        usecase.delete_user(other_id, current_user)


def test_delete_user_not_found(usecase, user_repository_mock, current_user):
    user_repository_mock.get_user_by_id.return_value = None

    with pytest.raises(UserNotFoundException):
        usecase.delete_user(current_user.id, current_user)
