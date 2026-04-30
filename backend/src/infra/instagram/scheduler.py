import logging
from apscheduler.schedulers.background import BackgroundScheduler
from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.infra.db.repositories.instagram_post_repository_interface import InstagramPostRepository
from backend.src.infra.db.repositories.decorated_cake_repository_interface import DecoratedCakeRepository
from backend.src.infra.db.repositories.app_config_repository import AppConfigRepository
from backend.src.usecases.instagram_usecases import InstagramPostUsecase
from backend.src.infra.instagram.instagram_client import fetch_instagram_posts, refresh_instagram_token
from backend.src.config.settings import settings

logger = logging.getLogger(__name__)

INSTAGRAM_TOKEN_KEY = "instagram_access_token"


def refresh_token_job() -> None:
    logger.info("Running Instagram token refresh job")
    new_token = refresh_instagram_token(settings.INSTAGRAM_ACCESS_TOKEN)
    if new_token:
        settings.INSTAGRAM_ACCESS_TOKEN = new_token
        with DBConnectionHandler() as db:
            AppConfigRepository(db).set(INSTAGRAM_TOKEN_KEY, new_token)
        logger.info("Instagram token refreshed and persisted to database")
    else:
        logger.warning("Instagram token refresh job failed — token may expire soon")


def sync_instagram_job() -> dict:
    logger.info("Running Instagram sync job")
    synced = 0
    skipped = 0
    errors = 0

    if not settings.INSTAGRAM_ACCESS_TOKEN:
        logger.error("Instagram sync aborted: INSTAGRAM_ACCESS_TOKEN is not configured")
        return {"synced": 0, "skipped": 0, "errors": 0, "error": "Token not configured"}

    with DBConnectionHandler() as db:
        instagram_repo = InstagramPostRepository(db)
        decorated_cake_repo = DecoratedCakeRepository(db)
        usecase = InstagramPostUsecase(instagram_repo, decorated_cake_repo)

        posts = fetch_instagram_posts(settings.INSTAGRAM_ACCESS_TOKEN)
        logger.info("Fetched posts from Instagram", extra={"count": len(posts)})

        for post in posts:
            media_url = post.get("media_url")
            permalink = post.get("permalink")
            if not media_url or not permalink:
                logger.warning("Skipping post without media_url or permalink", extra={"instagram_id": post.get("id")})
                skipped += 1
                continue
            try:
                usecase.sync_post(
                    instagram_id=post["id"],
                    caption=post.get("caption"),
                    media_url=media_url,
                    permalink=permalink,
                )
                synced += 1
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Failed to sync post", extra={"instagram_id": post.get("id"), "error": str(e)})
                errors += 1

        usecase.refresh_featured_status()

    logger.info("Instagram sync job completed", extra={"synced": synced, "skipped": skipped, "errors": errors})
    return {"synced": synced, "skipped": skipped, "errors": errors}


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_instagram_job, "interval", hours=6, id="instagram_sync")
    # Refresh token every 50 days (tokens last 60 days, refresh early for safety)
    scheduler.add_job(refresh_token_job, "interval", days=50, id="instagram_token_refresh")
    scheduler.start()
    logger.info("Scheduler started")
    return scheduler
