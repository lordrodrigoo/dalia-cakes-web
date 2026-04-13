# pylint: disable=unused-argument
from uuid import UUID
from fastapi import Request, status
from fastapi.responses import JSONResponse


class InstagramPostNotFoundException(Exception):
    def __init__(self, post_id: UUID):
        self.post_id = post_id
        self.message = f"Instagram post with ID '{post_id}' not found."
        super().__init__(self.message)


async def instagram_post_not_found_exception_handler(request: Request, exc: InstagramPostNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )


class DecoratedCakeNotFoundException(Exception):
    def __init__(self, subcategory_id: UUID):
        self.subcategory_id = subcategory_id
        self.message = f"Decorated cake subcategory with ID '{subcategory_id}' not found."
        super().__init__(self.message)


async def decorated_cake_not_found_exception_handler(request: Request, exc: DecoratedCakeNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )
