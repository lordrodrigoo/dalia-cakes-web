# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
from uuid import uuid4
from unittest.mock import MagicMock
import pytest
from backend.src.dto.request.admin_request import AdminRequest
from backend.src.exceptions.exception_handlers_admin import (
    EmailAlreadyExistsException,
    AdminNotFoundException,
    UsernameAlreadyExistsException,
    AdminPermissionDeniedException,
)


# ──────────────────────────────────────────────
# create_admin
# ──────────────────────────────────────────────

def test_create_admin_success(usecase, admin_repository_mock, valid_user_data, fake_user_domain, owner_user):
    admin_repository_mock.get_admin_by_email.return_value = None
    admin_repository_mock.get_admin_by_username.return_value = None
    admin_repository_mock.create_admin.return_value = fake_user_domain

    request = AdminRequest(**valid_user_data)
    result = usecase.create_admin(request, owner_user)

    assert result.email == valid_user_data["email"]
    assert result.username == valid_user_data["username"]
    admin_repository_mock.create_admin.assert_called_once()


def test_create_admin_permission_denied(usecase, valid_user_data, current_user):
    """Non-OWNER user tenta criar admin → AdminPermissionDeniedException."""
    request = AdminRequest(**valid_user_data)
    with pytest.raises(AdminPermissionDeniedException):
        usecase.create_admin(request, current_user)


def test_create_admin_email_already_exists(usecase, admin_repository_mock, valid_user_data, fake_user_domain, owner_user):
    admin_repository_mock.get_admin_by_email.return_value = fake_user_domain

    request = AdminRequest(**valid_user_data)
    with pytest.raises(EmailAlreadyExistsException) as exc_info:
        usecase.create_admin(request, owner_user)

    assert valid_user_data["email"] in exc_info.value.message


def test_create_admin_username_already_exists(usecase, admin_repository_mock, valid_user_data, fake_user_domain, owner_user):
    admin_repository_mock.get_admin_by_email.return_value = None
    admin_repository_mock.get_admin_by_username.return_value = fake_user_domain

    request = AdminRequest(**valid_user_data)
    with pytest.raises(UsernameAlreadyExistsException) as exc_info:
        usecase.create_admin(request, owner_user)

    assert valid_user_data["username"] in exc_info.value.message


# ──────────────────────────────────────────────
# get_admin_by_id
# ──────────────────────────────────────────────

def test_get_admin_by_id_success(usecase, admin_repository_mock, fake_user_domain):
    admin_repository_mock.get_admin_by_id.return_value = fake_user_domain

    result = usecase.get_admin_by_id(fake_user_domain.id)

    assert result.id == fake_user_domain.id
    admin_repository_mock.get_admin_by_id.assert_called_once_with(fake_user_domain.id)


def test_get_admin_by_id_not_found(usecase, admin_repository_mock):
    admin_repository_mock.get_admin_by_id.return_value = None

    with pytest.raises(AdminNotFoundException):
        usecase.get_admin_by_id("non-existent-id")


# ──────────────────────────────────────────────
# get_admin_by_email
# ──────────────────────────────────────────────

def test_get_admin_by_email_success(usecase, admin_repository_mock, fake_user_domain):
    admin_repository_mock.get_admin_by_email.return_value = fake_user_domain

    result = usecase.get_admin_by_email(fake_user_domain.email)

    assert result.email == fake_user_domain.email


def test_get_admin_by_email_not_found(usecase, admin_repository_mock):
    admin_repository_mock.get_admin_by_email.return_value = None

    with pytest.raises(AdminNotFoundException) as exc_info:
        usecase.get_admin_by_email("notfound@example.com")

    assert "notfound@example.com" in exc_info.value.message


# ──────────────────────────────────────────────
# update_admin
# ──────────────────────────────────────────────

def test_update_admin_success(usecase, admin_repository_mock, valid_user_data, fake_user_domain, current_user):
    admin_repository_mock.get_admin_by_id.return_value = fake_user_domain
    admin_repository_mock.get_admin_by_email.return_value = None
    admin_repository_mock.get_admin_by_username.return_value = None
    admin_repository_mock.update_admin.return_value = fake_user_domain

    request = AdminRequest(**valid_user_data)
    result = usecase.update_admin(current_user.id, request, current_user)

    assert result.id == fake_user_domain.id
    admin_repository_mock.update_admin.assert_called_once()


def test_update_admin_email_and_username_changed(usecase, admin_repository_mock, valid_user_data, fake_user_domain, current_user):
    """Email e username diferentes e sem conflito → user.email e user.username são atribuídos."""
    fake_user_domain.email = "old@example.com"
    fake_user_domain.username = "old.username"
    valid_user_data["email"] = "new@example.com"
    valid_user_data["username"] = "new.username"

    admin_repository_mock.get_admin_by_id.return_value = fake_user_domain
    admin_repository_mock.get_admin_by_email.return_value = None
    admin_repository_mock.get_admin_by_username.return_value = None
    admin_repository_mock.update_admin.return_value = fake_user_domain

    request = AdminRequest(**valid_user_data)
    result = usecase.update_admin(current_user.id, request, current_user)

    assert result is not None
    admin_repository_mock.update_admin.assert_called_once()


def test_update_admin_permission_denied(usecase, admin_repository_mock, valid_user_data, current_user):
    other_id = uuid4()

    request = AdminRequest(**valid_user_data)
    with pytest.raises(AdminPermissionDeniedException):
        usecase.update_admin(other_id, request, current_user)


def test_update_admin_not_found(usecase, admin_repository_mock, valid_user_data, current_user):
    admin_repository_mock.get_admin_by_id.return_value = None

    request = AdminRequest(**valid_user_data)
    with pytest.raises(AdminNotFoundException):
        usecase.update_admin(current_user.id, request, current_user)


def test_update_admin_email_conflict(usecase, admin_repository_mock, valid_user_data, fake_user_domain, current_user):
    other_user = MagicMock()
    other_user.email = "other@example.com"

    fake_user_domain.email = "old@example.com"
    valid_user_data["email"] = "new@example.com"
    valid_user_data["email"] = "new@example.com"

    admin_repository_mock.get_admin_by_id.return_value = fake_user_domain
    admin_repository_mock.get_admin_by_email.return_value = other_user

    request = AdminRequest(**valid_user_data)
    with pytest.raises(EmailAlreadyExistsException):
        usecase.update_admin(current_user.id, request, current_user)


def test_update_admin_username_conflict(usecase, admin_repository_mock, valid_user_data, fake_user_domain, current_user):
    other_user = MagicMock()
    other_user.username = "other.user"

    fake_user_domain.username = "old.username"
    valid_user_data["username"] = "new.username"

    admin_repository_mock.get_admin_by_id.return_value = fake_user_domain
    admin_repository_mock.get_admin_by_email.return_value = None
    admin_repository_mock.get_admin_by_username.return_value = other_user

    request = AdminRequest(**valid_user_data)
    with pytest.raises(UsernameAlreadyExistsException):
        usecase.update_admin(current_user.id, request, current_user)


# ──────────────────────────────────────────────
# delete_admin
# ──────────────────────────────────────────────

def test_delete_admin_success(usecase, admin_repository_mock, fake_user_domain, current_user):
    admin_repository_mock.get_admin_by_id.return_value = fake_user_domain

    usecase.delete_admin(current_user.id, current_user)

    admin_repository_mock.delete_admin.assert_called_once_with(current_user.id)


def test_delete_admin_permission_denied(usecase, admin_repository_mock, current_user):
    other_id = uuid4()

    with pytest.raises(AdminPermissionDeniedException):
        usecase.delete_admin(other_id, current_user)


def test_delete_admin_not_found(usecase, admin_repository_mock, current_user):
    admin_repository_mock.get_admin_by_id.return_value = None

    with pytest.raises(AdminNotFoundException):
        usecase.delete_admin(current_user.id, current_user)
