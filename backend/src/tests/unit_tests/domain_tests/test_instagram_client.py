# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock, patch
import httpx
from backend.src.infra.instagram.instagram_client import fetch_instagram_posts


# ──────────────────────────────────────────────
# fetch_instagram_posts — sucesso
# ──────────────────────────────────────────────

def test_fetch_instagram_posts_success():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "123456789",
                "caption": "Bolo lindo #boloFeminino",
                "media_url": "https://example.com/img.jpg",
                "permalink": "https://instagram.com/p/abc",
                "timestamp": "2026-04-13T10:00:00Z",
            }
        ]
    }
    mock_response.raise_for_status = MagicMock()

    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = mock_response

    with patch("backend.src.infra.instagram.instagram_client.httpx.Client", return_value=mock_client):
        result = fetch_instagram_posts("fake_token")

    assert len(result) == 1
    assert result[0]["id"] == "123456789"
    assert result[0]["caption"] == "Bolo lindo #boloFeminino"


def test_fetch_instagram_posts_empty_data():
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_response.raise_for_status = MagicMock()

    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = mock_response

    with patch("backend.src.infra.instagram.instagram_client.httpx.Client", return_value=mock_client):
        result = fetch_instagram_posts("fake_token")

    assert result == []


def test_fetch_instagram_posts_no_data_key():
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status = MagicMock()

    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = mock_response

    with patch("backend.src.infra.instagram.instagram_client.httpx.Client", return_value=mock_client):
        result = fetch_instagram_posts("fake_token")

    assert result == []


# ──────────────────────────────────────────────
# fetch_instagram_posts — erro HTTP
# ──────────────────────────────────────────────

def test_fetch_instagram_posts_http_error():
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get.side_effect = httpx.HTTPError("connection error")

    with patch("backend.src.infra.instagram.instagram_client.httpx.Client", return_value=mock_client):
        result = fetch_instagram_posts("fake_token")

    assert result == []


def test_fetch_instagram_posts_status_error():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "401 Unauthorized",
        request=MagicMock(),
        response=MagicMock(),
    )

    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = mock_response

    with patch("backend.src.infra.instagram.instagram_client.httpx.Client", return_value=mock_client):
        result = fetch_instagram_posts("invalid_token")

    assert result == []
