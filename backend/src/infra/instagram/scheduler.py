import logging
from apscheduler.schedulers.background import BackgroundScheduler
from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.infra.db.repositories.instagram_post_repository_interface import InstagramPostRepository
from backend.src.infra.db.repositories.decorated_cake_repository_interface import DecoratedCakeRepository
from backend.src.usecases.instagram_usecases import InstagramPostUsecase
from backend.src.infra.instagram.instagram_client import fetch_instagram_posts
from backend.src.config.settings import Settings

logger = logging.getLogger(__name__)


def sync_instagram_job() -> None:
    logger.info("Running Instagram sync job")
    with DBConnectionHandler() as db:
        instagram_repo = InstagramPostRepository(db)
        decorated_cake_repo = DecoratedCakeRepository(db)
        usecase = InstagramPostUsecase(instagram_repo, decorated_cake_repo)

        posts = fetch_instagram_posts(Settings.INSTAGRAM_ACCESS_TOKEN)
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
    scheduler.start()
    logger.info("Scheduler started")
    return scheduler
