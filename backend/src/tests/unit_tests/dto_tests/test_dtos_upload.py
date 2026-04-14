from backend.src.dto.response.upload_response import UploadResponse


# ──────────────────────────────────────────────
# UploadResponse
# ──────────────────────────────────────────────

def test_upload_response_valid():
    resp = UploadResponse(url="https://bucket.s3.us-east-1.amazonaws.com/products/abc.webp")
    assert resp.url == "https://bucket.s3.us-east-1.amazonaws.com/products/abc.webp"


def test_upload_response_url_is_string():
    resp = UploadResponse(url="https://example.com/image.webp")
    assert isinstance(resp.url, str)
