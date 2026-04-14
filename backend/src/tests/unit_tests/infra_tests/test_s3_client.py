# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock, patch
import pytest
from botocore.exceptions import ClientError, BotoCoreError
from backend.src.infra.s3.s3_client import S3Client


@pytest.fixture
def boto3_client_mock():
    return MagicMock()


@pytest.fixture
def s3_client(boto3_client_mock):
    with patch("backend.src.infra.s3.s3_client.boto3.client", return_value=boto3_client_mock):
        client = S3Client(
            access_key="fake_key",
            secret_key="fake_secret",
            bucket="my-bucket",
            region="us-east-1",
        )
    client._client = boto3_client_mock
    return client


# ──────────────────────────────────────────────
# upload — sucesso
# ──────────────────────────────────────────────

def test_upload_returns_public_url(s3_client, boto3_client_mock):
    boto3_client_mock.put_object.return_value = {}
    url = s3_client.upload(b"fake_image_bytes", "products")
    assert url.startswith("https://my-bucket.s3.us-east-1.amazonaws.com/products/")
    assert url.endswith(".webp")


def test_upload_calls_put_object(s3_client, boto3_client_mock):
    boto3_client_mock.put_object.return_value = {}
    s3_client.upload(b"fake_bytes", "categories")
    boto3_client_mock.put_object.assert_called_once()


def test_upload_uses_correct_bucket(s3_client, boto3_client_mock):
    boto3_client_mock.put_object.return_value = {}
    s3_client.upload(b"fake_bytes", "products")
    call_kwargs = boto3_client_mock.put_object.call_args[1]
    assert call_kwargs["Bucket"] == "my-bucket"


def test_upload_uses_correct_content_type(s3_client, boto3_client_mock):
    boto3_client_mock.put_object.return_value = {}
    s3_client.upload(b"fake_bytes", "products", content_type="image/webp")
    call_kwargs = boto3_client_mock.put_object.call_args[1]
    assert call_kwargs["ContentType"] == "image/webp"


def test_upload_key_contains_folder(s3_client, boto3_client_mock):
    boto3_client_mock.put_object.return_value = {}
    s3_client.upload(b"fake_bytes", "products")
    call_kwargs = boto3_client_mock.put_object.call_args[1]
    assert call_kwargs["Key"].startswith("products/")


def test_upload_key_ends_with_webp(s3_client, boto3_client_mock):
    boto3_client_mock.put_object.return_value = {}
    s3_client.upload(b"fake_bytes", "categories")
    call_kwargs = boto3_client_mock.put_object.call_args[1]
    assert call_kwargs["Key"].endswith(".webp")


def test_upload_generates_unique_keys(s3_client, boto3_client_mock):
    boto3_client_mock.put_object.return_value = {}
    url1 = s3_client.upload(b"bytes1", "products")
    url2 = s3_client.upload(b"bytes2", "products")
    assert url1 != url2


# ──────────────────────────────────────────────
# upload — erros
# ──────────────────────────────────────────────

def test_upload_raises_on_client_error(s3_client, boto3_client_mock):
    boto3_client_mock.put_object.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Access Denied"}},
        "PutObject"
    )
    with pytest.raises(ClientError):
        s3_client.upload(b"fake_bytes", "products")


def test_upload_raises_on_botocore_error(s3_client, boto3_client_mock):
    boto3_client_mock.put_object.side_effect = BotoCoreError()
    with pytest.raises(BotoCoreError):
        s3_client.upload(b"fake_bytes", "products")
