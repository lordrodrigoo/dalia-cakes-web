import io
import logging
from PIL import Image
from botocore.exceptions import BotoCoreError, ClientError
from backend.src.infra.s3.s3_client import S3Client
from backend.src.exceptions.exception_handlers_upload import (
    ImageUploadException,
    InvalidUploadFolderException,
    InvalidImageTypeException,
)

logger = logging.getLogger(__name__)

IMAGE_SIZES = {
    "products": (800, 800),
    "categories": (1200, 800),
    "instagram": (800, 800),
}
ALLOWED_FOLDERS = set(IMAGE_SIZES.keys())
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
DEFAULT_SIZE = (800, 800)
QUALITY = 80


class UploadUsecase:
    def __init__(self, s3_client: S3Client):
        self._s3 = s3_client

    def upload_image(self, file_bytes: bytes, folder: str, content_type: str) -> str:
        if folder not in ALLOWED_FOLDERS:
            raise InvalidUploadFolderException()
        if content_type not in ALLOWED_CONTENT_TYPES:
            raise InvalidImageTypeException()

        width, height = IMAGE_SIZES.get(folder, DEFAULT_SIZE)
        processed = self._process_image(file_bytes, width, height)
        try:
            url = self._s3.upload(processed, folder)
        except (BotoCoreError, ClientError) as exc:
            logger.error("Upload to S3 failed: %s", exc)
            raise ImageUploadException() from exc
        return url

    def delete_image(self, url: str) -> None:
        if not url:
            return
        try:
            key = "/".join(url.split(".amazonaws.com/")[1:]) if ".amazonaws.com/" in url else None
            if key:
                self._s3.delete(key)
        except (BotoCoreError, ClientError) as exc:
            logger.warning("S3 image delete failed, continuing: %s", exc)

    def _process_image(self, file_bytes: bytes, width: int, height: int) -> bytes:
        img = Image.open(io.BytesIO(file_bytes))
        img = img.convert("RGB")
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        output = io.BytesIO()
        img.save(output, format="WEBP", quality=QUALITY)
        return output.getvalue()
