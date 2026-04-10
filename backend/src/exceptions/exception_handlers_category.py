# pylint: disable=unused-argument
from uuid import UUID
from fastapi import Request, status
from fastapi.responses import JSONResponse


class CategoryNotFoundException(Exception):
    def __init__(self, category_id: UUID = None, slug: str = None):
        if slug:
            self.message = f"Category with slug '{slug}' not found."
        else:
            self.message = f"Category with ID '{category_id}' not found."
        super().__init__(self.message)

async def category_not_found_exception_handler(request: Request, exc: CategoryNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )

class CategoryNameAlreadyExistsException(Exception):
    def __init__(self, name: str):
        self.name = name
        self.message = f"Category with name '{name}' already exists."
        super().__init__(self.message)

async def category_name_already_exists_exception_handler(request: Request, exc: CategoryNameAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": exc.message}
    )

class CategorySlugAlreadyExistsException(Exception):
    def __init__(self, slug: str):
        self.slug = slug
        self.message = f"Category with slug '{slug}' already exists."
        super().__init__(self.message)


async def category_slug_already_exists_exception_handler(request: Request, exc: CategorySlugAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": exc.message}
    )
