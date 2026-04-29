import io
import uuid
import logging
import boto3
from botocore.exceptions import ClientError, BotoCoreError


logger = logging.getLogger(__name__)


class S3Client:
    def __init__(self, access_key: str, secret_key: str, bucket: str, region: str):
        self._bucket = bucket
        self._region = region
        self._client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def upload(self, file_bytes: bytes, folder: str, content_type: str = "image/webp") -> str:
        key = f"{folder}/{uuid.uuid4()}.webp"
        try:
            self._client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=io.BytesIO(file_bytes),
                ContentType=content_type,
            )
        except (BotoCoreError, ClientError) as exc:
            logger.error("S3 upload failed: %s", exc)
            raise

        return f"https://{self._bucket}.s3.{self._region}.amazonaws.com/{key}"

    def delete(self, key: str) -> None:
        try:
            self._client.delete_object(Bucket=self._bucket, Key=key)
        except (BotoCoreError, ClientError) as exc:
            logger.error("S3 delete failed: %s", exc)
            raise
