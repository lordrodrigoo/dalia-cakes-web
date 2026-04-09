# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
from unittest.mock import patch
from unittest.mock import MagicMock
import pytest
from backend.src.dto.response.token_response import TokenResponse
from backend.src.exceptions.exception_handlers_auth import InvalidCredentialsException
from backend.src.config.security import DUMMY_HASH

# ──────────────────────────────────────────────
# login
# ──────────────────────────────────────────────

@patch("backend.src.usecases.auth_usecases.create_refresh_token", return_value="refresh_tok")
@patch("backend.src.usecases.auth_usecases.create_access_token", return_value="access_tok")
@patch("backend.src.usecases.auth_usecases.verify_password", return_value=True)
def test_login_success(mock_verify, mock_access, mock_refresh, auth_usecase, auth_repository_mock, fake_auth_user):
    auth_repository_mock.get_user_by_username.return_value = fake_auth_user

    result = auth_usecase.login("rodrigo.souza", "P@ssw0rd1")

    assert isinstance(result, TokenResponse)
    assert result.access_token == "access_tok"
    assert result.refresh_token == "refresh_tok"
    assert result.token_type == "bearer"


def test_login_user_not_found(auth_usecase, auth_repository_mock):
    auth_repository_mock.get_user_by_username.return_value = None

    with pytest.raises(InvalidCredentialsException):
        auth_usecase.login("unknown", "P@ssw0rd1")


@patch("backend.src.usecases.auth_usecases.verify_password", return_value=False)
def test_login_user_not_found_calls_dummy_hash(mock_verify, auth_usecase, auth_repository_mock):
    """Garante que verify_password é chamado com DUMMY_HASH mesmo quando o usuário não existe (previne timing attack)."""
    auth_repository_mock.get_user_by_username.return_value = None

    with pytest.raises(InvalidCredentialsException):
        auth_usecase.login("unknown", "P@ssw0rd1")

    mock_verify.assert_called_once_with("P@ssw0rd1", DUMMY_HASH)


@patch("backend.src.usecases.auth_usecases.verify_password", return_value=False)
def test_login_wrong_password(mock_verify, auth_usecase, auth_repository_mock, fake_auth_user):
    auth_repository_mock.get_user_by_username.return_value = fake_auth_user

    with pytest.raises(InvalidCredentialsException):
        auth_usecase.login("rodrigo.souza", "WrongPass1!")


# ──────────────────────────────────────────────
# refresh_token
# ──────────────────────────────────────────────

@patch("backend.src.usecases.auth_usecases.create_access_token", return_value="new_access_tok")
@patch("backend.src.usecases.auth_usecases.verify_token")
def test_refresh_token_success(mock_verify_token, mock_access, auth_usecase, auth_repository_mock, fake_auth_user):
    payload = MagicMock()
    payload.sub = fake_auth_user.id
    mock_verify_token.return_value = payload
    auth_repository_mock.get_user_by_id.return_value = fake_auth_user

    result = auth_usecase.refresh_token("valid_refresh_token")

    assert isinstance(result, TokenResponse)
    assert result.access_token == "new_access_tok"
    assert result.refresh_token == "valid_refresh_token"


@patch("backend.src.usecases.auth_usecases.verify_token")
def test_refresh_token_user_not_found(mock_verify_token, auth_usecase, auth_repository_mock, fake_auth_user):
    payload = MagicMock()
    payload.sub = fake_auth_user.id
    mock_verify_token.return_value = payload
    auth_repository_mock.get_user_by_id.return_value = None

    with pytest.raises(InvalidCredentialsException):
        auth_usecase.refresh_token("some_token")
