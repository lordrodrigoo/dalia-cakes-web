# pylint: disable=redefined-outer-name, protected-access
from unittest.mock import MagicMock
import io
import pytest
from PIL import Image
from botocore.exceptions import ClientError, BotoCoreError
from backend.src.usecases.upload_usecases import UploadUsecase
from backend.src.exceptions.exception_handlers_upload import (
    ImageUploadException,
    InvalidUploadFolderException,
    InvalidImageTypeException,
)


def make_jpeg_bytes(width=1000, height=1000) -> bytes:
    img = Image.new("RGB", (width, height), color=(200, 100, 50))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def make_png_bytes_with_alpha(width=1000, height=1000) -> bytes:
    img = Image.new("RGBA", (width, height), color=(200, 100, 50, 128))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@pytest.fixture
def s3_mock():
    return MagicMock()


@pytest.fixture
def upload_usecase(s3_mock):
    return UploadUsecase(s3_client=s3_mock)


# ──────────────────────────────────────────────
# Validação de folder
# ──────────────────────────────────────────────

def test_upload_invalid_folder_raises(upload_usecase):
    with pytest.raises(InvalidUploadFolderException):
        upload_usecase.upload_image(make_jpeg_bytes(), "invalid_folder", "image/jpeg")


def test_upload_valid_folder_products_ok(upload_usecase, s3_mock):
    s3_mock.upload.return_value = "https://bucket.s3.us-east-1.amazonaws.com/products/img.webp"
    url = upload_usecase.upload_image(make_jpeg_bytes(), "products", "image/jpeg")
    assert "products" in url


def test_upload_valid_folder_categories_ok(upload_usecase, s3_mock):
    s3_mock.upload.return_value = "https://bucket.s3.us-east-1.amazonaws.com/categories/img.webp"
    url = upload_usecase.upload_image(make_jpeg_bytes(), "categories", "image/jpeg")
    assert "categories" in url


# ──────────────────────────────────────────────
# Validação de formato (via PIL)
# ──────────────────────────────────────────────

def test_upload_invalid_image_bytes_raises(upload_usecase):
    with pytest.raises(InvalidImageTypeException):
        upload_usecase.upload_image(b"this is not an image", "products", "application/pdf")


def test_upload_jpeg_accepted(upload_usecase, s3_mock):
    s3_mock.upload.return_value = "https://bucket.s3.amazonaws.com/products/x.webp"
    url = upload_usecase.upload_image(make_jpeg_bytes(), "products", "image/jpeg")
    assert url.startswith("https://")


def test_upload_png_accepted(upload_usecase, s3_mock):
    s3_mock.upload.return_value = "https://bucket.s3.amazonaws.com/products/x.webp"
    url = upload_usecase.upload_image(make_png_bytes_with_alpha(), "products", "image/png")
    assert url.startswith("https://")


def test_upload_webp_accepted(upload_usecase, s3_mock):
    # create a webp
    img = Image.new("RGB", (100, 100))
    buf = io.BytesIO()
    img.save(buf, format="WEBP")
    s3_mock.upload.return_value = "https://bucket.s3.amazonaws.com/products/x.webp"
    url = upload_usecase.upload_image(buf.getvalue(), "products", "image/webp")
    assert url.startswith("https://")


# ──────────────────────────────────────────────
# Processamento de imagem
# ──────────────────────────────────────────────

def test_process_image_outputs_webp_bytes(upload_usecase):
    result = upload_usecase._process_image(make_jpeg_bytes(), 800, 800)
    img = Image.open(io.BytesIO(result))
    assert img.format == "WEBP"


def test_process_image_resizes_to_products(upload_usecase):
    result = upload_usecase._process_image(make_jpeg_bytes(1200, 1200), 800, 800)
    img = Image.open(io.BytesIO(result))
    assert img.size == (800, 800)


def test_process_image_resizes_to_categories(upload_usecase):
    result = upload_usecase._process_image(make_jpeg_bytes(2000, 1000), 1200, 600)
    img = Image.open(io.BytesIO(result))
    assert img.size == (1200, 600)


def test_process_image_converts_rgba_to_rgb(upload_usecase):
    result = upload_usecase._process_image(make_png_bytes_with_alpha(), 800, 800)
    img = Image.open(io.BytesIO(result))
    assert img.mode == "RGB"


# ──────────────────────────────────────────────
# Erro no S3
# ──────────────────────────────────────────────

def test_upload_s3_client_error_raises_image_upload_exception(upload_usecase, s3_mock):
    s3_mock.upload.side_effect = ClientError(
        {"Error": {"Code": "NoSuchBucket", "Message": "Bucket not found"}},
        "PutObject"
    )
    with pytest.raises(ImageUploadException):
        upload_usecase.upload_image(make_jpeg_bytes(), "products", "image/jpeg")


def test_upload_s3_botocore_error_raises_image_upload_exception(upload_usecase, s3_mock):
    s3_mock.upload.side_effect = BotoCoreError()
    with pytest.raises(ImageUploadException):
        upload_usecase.upload_image(make_jpeg_bytes(), "products", "image/jpeg")


# ──────────────────────────────────────────────
# S3 upload é chamado com os bytes processados
# ──────────────────────────────────────────────

def test_upload_calls_s3_with_correct_folder(upload_usecase, s3_mock):
    s3_mock.upload.return_value = "https://bucket.s3.amazonaws.com/products/x.webp"
    upload_usecase.upload_image(make_jpeg_bytes(), "products", "image/jpeg")
    s3_mock.upload.assert_called_once()
    call_kwargs = s3_mock.upload.call_args
    assert call_kwargs[0][1] == "products"


def test_upload_returns_url_from_s3(upload_usecase, s3_mock):
    expected_url = "https://bucket.s3.us-east-1.amazonaws.com/products/uuid.webp"
    s3_mock.upload.return_value = expected_url
    url = upload_usecase.upload_image(make_jpeg_bytes(), "products", "image/jpeg")
    assert url == expected_url
