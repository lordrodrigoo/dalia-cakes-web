import logging
import httpx

logger = logging.getLogger(__name__)

INSTAGRAM_GRAPH_URL = "https://graph.instagram.com/v21.0"
INSTAGRAM_REFRESH_URL = "https://graph.instagram.com/refresh_access_token"
MAX_PAGES = 10


def fetch_instagram_posts(access_token: str) -> list[dict]:
    """Fetch all recent media from Instagram Graph API, following pagination."""
    url = f"{INSTAGRAM_GRAPH_URL}/me/media"
    params = {
        "fields": "id,caption,media_url,permalink,timestamp",
        "access_token": access_token,
    }
    all_posts: list[dict] = []
    try:
        with httpx.Client(timeout=10.0) as client:
            for _ in range(MAX_PAGES):
                response = client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                all_posts.extend(data.get("data", []))
                next_url = data.get("paging", {}).get("next")
                if not next_url:
                    break
                url = next_url
                params = {}
    except httpx.HTTPError as e:
        logger.error("Failed to fetch Instagram posts", extra={"error": str(e)})
    return all_posts


def refresh_instagram_token(access_token: str) -> str | None:
    """Refresh a long-lived Instagram access token. Returns the new token or None on failure."""
    params = {
        "grant_type": "ig_refresh_token",
        "access_token": access_token,
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(INSTAGRAM_REFRESH_URL, params=params)
            response.raise_for_status()
            data = response.json()
            new_token = data.get("access_token")
            expires_in = data.get("expires_in")
            logger.info("Instagram token refreshed", extra={"expires_in": expires_in})
            return new_token
    except httpx.HTTPError as e:
        logger.error("Failed to refresh Instagram token", extra={"error": str(e)})
        return None
