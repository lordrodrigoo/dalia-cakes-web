import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.infra.db.repositories.instagram_post_repository_interface import InstagramPostRepository
from backend.src.infra.db.repositories.decorated_cake_repository_interface import DecoratedCakeRepository
from backend.src.usecases.instagram_usecases import InstagramPostUsecase
from backend.src.infra.instagram.instagram_client import fetch_instagram_posts, refresh_instagram_token
from backend.src.config.settings import settings

logger = logging.getLogger(__name__)

# How many days before expiry to trigger a proactive token refresh
TOKEN_REFRESH_THRESHOLD_DAYS = 10


def refresh_token_job() -> None:
    logger.info("Running Instagram token refresh job")
    new_token = refresh_instagram_token(settings.INSTAGRAM_ACCESS_TOKEN)
    if new_token:
        # Persist updated token to environment so next sync uses it
        os.environ["INSTAGRAM_ACCESS_TOKEN"] = new_token
        settings.INSTAGRAM_ACCESS_TOKEN = new_token
        logger.info("Instagram token updated in memory")
    else:
        logger.warning("Instagram token refresh job failed — token may expire soon")


def sync_instagram_job() -> None:
    logger.info("Running Instagram sync job")
    with DBConnectionHandler() as db:
        instagram_repo = InstagramPostRepository(db)
        decorated_cake_repo = DecoratedCakeRepository(db)
        usecase = InstagramPostUsecase(instagram_repo, decorated_cake_repo)

        posts = fetch_instagram_posts(settings.INSTAGRAM_ACCESS_TOKEN)
        for post in posts:
            usecase.sync_post(
                instagram_id=post["id"],
                caption=post.get("caption"),
                media_url=post["media_url"],
                permalink=post["permalink"],
            )

        usecase.refresh_featured_status()
    logger.info("Instagram sync job completed")


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_instagram_job, "interval", hours=6, id="instagram_sync")
    # Refresh token every 50 days (tokens last 60 days, refresh early for safety)
    scheduler.add_job(refresh_token_job, "interval", days=50, id="instagram_token_refresh")
    scheduler.start()
    logger.info("Scheduler started")
    return scheduler
