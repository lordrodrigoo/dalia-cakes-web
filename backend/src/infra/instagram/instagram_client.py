import logging
import httpx

logger = logging.getLogger(__name__)

INSTAGRAM_GRAPH_URL = "https://graph.instagram.com/v21.0"


def fetch_instagram_posts(access_token: str) -> list[dict]:
    """Fetch recent media from Instagram Graph API."""
    url = f"{INSTAGRAM_GRAPH_URL}/me/media"
    params = {
        "fields": "id,caption,media_url,permalink,timestamp",
        "access_token": access_token,
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
    except httpx.HTTPError as e:
        logger.error("Failed to fetch Instagram posts", extra={"error": str(e)})
        return []
