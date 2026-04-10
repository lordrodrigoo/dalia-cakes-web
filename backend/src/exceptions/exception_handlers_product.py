# pylint: disable=unused-argument
from uuid import UUID
from fastapi import Request, status
from fastapi.responses import JSONResponse


class ProductNotFoundException(Exception):
    def __init__(self, product_id: UUID):
        self.product_id = product_id
        self.message = f"Product with ID '{product_id}' not found."
        super().__init__(self.message)


async def product_not_found_exception_handler(request: Request, exc: ProductNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )


class ProductCategoryNotFoundException(Exception):
    def __init__(self, category_id: UUID):
        self.category_id = category_id
        self.message = f"Category with ID '{category_id}' not found."
        super().__init__(self.message)


async def product_category_not_found_exception_handler(request: Request, exc: ProductCategoryNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )
