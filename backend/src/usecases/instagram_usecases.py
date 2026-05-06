from uuid import UUID
import uuid as uuid_lib
from typing import Optional
import logging
from datetime import datetime, timezone, timedelta
from backend.src.domain.models.instagram_post import InstagramPost
from backend.src.domain.models.decorated_cake import DecoratedCake
from backend.src.domain.repositories.instagram_post_repository import InstagramPostRepositoryInterface
from backend.src.domain.repositories.decorated_cake_repository import DecoratedCakeRepositoryInterface
from backend.src.dto.request.instagram_post_request import UpdateSubcategoryRequest
from backend.src.dto.request.decorated_cake_request import DecoratedCakeRequest
from backend.src.dto.response.instagram_post_response import InstagramPostResponse
from backend.src.dto.response.decorated_cake_response import DecoratedCakeResponse
from backend.src.exceptions.exception_handlers_instagram import (
    InstagramPostNotFoundException,
    DecoratedCakeNotFoundException,
)
from backend.src.usecases.upload_usecases import UploadUsecase


logger = logging.getLogger(__name__)

FEATURED_DURATION_DAYS = 3


class InstagramPostUsecase:
    def __init__(
        self,
        instagram_post_repository: InstagramPostRepositoryInterface,
        decorated_cake_repository: DecoratedCakeRepositoryInterface,
        upload_usecase: UploadUsecase = None,
    ):
        self.instagram_post_repository = instagram_post_repository
        self.decorated_cake_repository = decorated_cake_repository
        self.upload_usecase = upload_usecase


    def _classify_post(self, caption: str | None, subcategories: list) -> Optional[UUID]:
        """Returns the subcategory_id for the post, or the 'outros' catch-all if nothing matches."""
        if caption:
            caption_lower = caption.lower()
            for sub in subcategories:
                if sub.slug == "outros":
                    continue
                if sub.hashtag.lower() in caption_lower:
                    return sub.id

        outros = next((s for s in subcategories if s.slug == "outros"), None)
        return outros.id if outros else None


    def sync_post(self, instagram_id: str, caption: str | None, media_url: str, permalink: str) -> InstagramPostResponse:
        existing = self.instagram_post_repository.get_by_instagram_id(instagram_id)
        if existing:
            # Sempre atualiza a URL — CDN do Instagram expira após alguns dias
            self.instagram_post_repository.refresh_media_url(existing.id, media_url, permalink)
            if existing.subcategory_id is not None:
                logger.info("Post already synced, skipping", extra={"instagram_id": instagram_id})
                return InstagramPostResponse(**existing.__dict__)
            # Existing but unclassified — try to reclassify now
            subcategories = self.decorated_cake_repository.get_all()
            subcategory_id = self._classify_post(caption, subcategories)
            if subcategory_id:
                updated = self.instagram_post_repository.update_subcategory(existing.id, subcategory_id)
                logger.info("Unclassified post reclassified on sync", extra={"instagram_id": instagram_id})
                return InstagramPostResponse(**updated.__dict__)
            return InstagramPostResponse(**existing.__dict__)

        subcategories = self.decorated_cake_repository.get_all()
        subcategory_id = self._classify_post(caption, subcategories)

        now = datetime.now(timezone.utc)
        post = InstagramPost(
            instagram_id=instagram_id,
            caption=caption,
            media_url=media_url,
            permalink=permalink,
            subcategory_id=subcategory_id,
            is_featured=True,
            synced_at=now,
            featured_until=now + timedelta(days=FEATURED_DURATION_DAYS),
        )
        saved = self.instagram_post_repository.save(post)
        logger.info("Post synced", extra={"instagram_id": instagram_id, "post_id": saved.id})
        return InstagramPostResponse(**saved.__dict__)


    def get_featured(self) -> list[InstagramPostResponse]:
        posts = self.instagram_post_repository.get_featured()
        return [InstagramPostResponse(**p.__dict__) for p in posts]


    def get_by_subcategory(self, subcategory_id: UUID) -> list[InstagramPostResponse]:
        if not self.decorated_cake_repository.get_by_id(subcategory_id):
            logger.warning("Decorated cake not found", extra={"subcategory_id": subcategory_id})
            raise DecoratedCakeNotFoundException(subcategory_id)
        posts = self.instagram_post_repository.get_by_subcategory(subcategory_id)
        return [InstagramPostResponse(**p.__dict__) for p in posts]


    def get_all(self) -> list[InstagramPostResponse]:
        posts = self.instagram_post_repository.get_all()
        return [InstagramPostResponse(**p.__dict__) for p in posts]



    def get_unclassified(self) -> list[InstagramPostResponse]:
        posts = self.instagram_post_repository.get_unclassified()
        return [InstagramPostResponse(**p.__dict__) for p in posts]


    def update_subcategory(self, post_id: UUID, request: UpdateSubcategoryRequest) -> InstagramPostResponse:
        if not self.decorated_cake_repository.get_by_id(request.subcategory_id):
            logger.warning("Decorated cake not found", extra={"subcategory_id": request.subcategory_id})
            raise DecoratedCakeNotFoundException(request.subcategory_id)

        updated = self.instagram_post_repository.update_subcategory(post_id, request.subcategory_id)
        if not updated:
            logger.warning("Instagram post not found for update", extra={"post_id": post_id})
            raise InstagramPostNotFoundException(post_id)

        logger.info("Post subcategory updated", extra={"post_id": post_id, "subcategory_id": request.subcategory_id})
        return InstagramPostResponse(**updated.__dict__)


    def delete(self, post_id: UUID) -> None:
        posts = self.instagram_post_repository.get_all()
        if not any(p.id == post_id for p in posts):
            logger.warning("Instagram post not found for delete", extra={"post_id": post_id})
            raise InstagramPostNotFoundException(post_id)
        post = next((p for p in posts if p.id == post_id), None)
        if self.upload_usecase and post and post.media_url:
            self.upload_usecase.delete_image(post.media_url)
        self.instagram_post_repository.delete(post_id)
        logger.info("Post deleted", extra={"post_id": post_id})


    def get_all_subcategories(self) -> list[DecoratedCakeResponse]:
        subcategories = self.decorated_cake_repository.get_all()
        return [DecoratedCakeResponse(**s.__dict__) for s in subcategories]


    def toggle_featured(self, post_id: UUID) -> InstagramPostResponse:
        posts = self.instagram_post_repository.get_all()
        post = next((p for p in posts if p.id == post_id), None)
        if not post:
            raise InstagramPostNotFoundException(post_id)
        now = datetime.now(timezone.utc)
        new_is_featured = not post.is_featured
        new_featured_until = now + timedelta(days=FEATURED_DURATION_DAYS) if new_is_featured else now
        updated = self.instagram_post_repository.update_featured_status(post_id, new_is_featured, new_featured_until)
        logger.info("Post featured toggled", extra={"post_id": post_id, "is_featured": new_is_featured})
        return InstagramPostResponse(**updated.__dict__)


    def refresh_featured_status(self) -> None:
        now = datetime.now(timezone.utc)
        posts = self.instagram_post_repository.get_all()
        for post in posts:
            if post.is_featured and post.featured_until < now:
                self.instagram_post_repository.update_featured_status(post.id, False, now)
                logger.info("Post featured status expired", extra={"post_id": post.id})


    def reclassify_unclassified_posts(self) -> int:
        """Tenta classificar todos os posts sem subcategoria. Retorna o total reclassificado."""
        unclassified = self.instagram_post_repository.get_unclassified()
        if not unclassified:
            return 0
        subcategories = self.decorated_cake_repository.get_all()
        count = 0
        for post in unclassified:
            subcategory_id = self._classify_post(post.caption, subcategories)
            if subcategory_id:
                self.instagram_post_repository.update_subcategory(post.id, subcategory_id)
                logger.info("Post reclassified", extra={"post_id": post.id, "subcategory_id": subcategory_id})
                count += 1
        return count


    def create_manual_post(
            self,
            media_url: str,
            subcategory_id: Optional[UUID] = None
    ) -> InstagramPostResponse:

        now = datetime.now(timezone.utc)
        post = InstagramPost(
            instagram_id=f"manual_{uuid_lib.uuid4().hex}",
            caption=None,
            media_url=media_url,
            permalink=media_url,
            subcategory_id=subcategory_id,
            is_featured=False,
            synced_at=now,
            featured_until=now,
        )
        saved = self.instagram_post_repository.save(post)
        logger.info("Manual post created", extra={"post_id": saved.id})
        return InstagramPostResponse(**saved.__dict__)

    # ── Subcategory CRUD ──────────────────────────────────────────────────────

    def create_subcategory(self, request: DecoratedCakeRequest) -> DecoratedCakeResponse:
        subcategory = DecoratedCake(
            name=request.name,
            slug=request.slug,
            hashtag=request.hashtag,
        )
        saved = self.decorated_cake_repository.save(subcategory)
        logger.info("Subcategory created", extra={"name": request.name})
        return DecoratedCakeResponse(**saved.__dict__)


    def update_subcategory_data(self, subcategory_id: UUID, request: DecoratedCakeRequest) -> DecoratedCakeResponse:
        existing = self.decorated_cake_repository.get_by_id(subcategory_id)
        if not existing:
            logger.warning("Decorated cake not found", extra={"subcategory_id": subcategory_id})
            raise DecoratedCakeNotFoundException(subcategory_id)
        existing.name = request.name
        existing.slug = request.slug
        existing.hashtag = request.hashtag
        updated = self.decorated_cake_repository.save(existing)
        logger.info("Subcategory updated", extra={"subcategory_id": subcategory_id})
        return DecoratedCakeResponse(**updated.__dict__)


    def delete_subcategory(self, subcategory_id: UUID) -> None:
        existing = self.decorated_cake_repository.get_by_id(subcategory_id)
        if not existing:
            logger.warning("Decorated cake not found", extra={"subcategory_id": subcategory_id})
            raise DecoratedCakeNotFoundException(subcategory_id)
        self.decorated_cake_repository.delete(subcategory_id)
        logger.info("Subcategory deleted", extra={"subcategory_id": subcategory_id})
