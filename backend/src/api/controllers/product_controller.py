from uuid import UUID
import os
import logging

from fastapi import APIRouter, Depends, status, Response

from backend.src.dto.request.product_request import ProductRequest
from backend.src.dto.response.product_response import ProductResponse
from backend.src.usecases.product_usecases import ProductUsecase
from backend.src.api.dependencies import get_product_usecase, get_current_user
from backend.src.dto.response.admin_response import AdminResponse


API_V1_PREFIX = os.getenv("API_V1_PREFIX", "/api/v1")
PRODUCT_PREFIX = f"{API_V1_PREFIX}/products"

router = APIRouter(prefix=PRODUCT_PREFIX, tags=["Products"])
logger = logging.getLogger(__name__)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_request: ProductRequest,
    response: Response,
    _: AdminResponse = Depends(get_current_user),
    product_usecase: ProductUsecase = Depends(get_product_usecase),
):
    """Authenticated endpoint to create a new product."""
    logger.info("Creating product", extra={"name": product_request.name})
    product = product_usecase.create_product(product_request)
    response.headers["Location"] = f"{PRODUCT_PREFIX}/{product.id}"
    return product


@router.get("", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def get_all_products(
    product_usecase: ProductUsecase = Depends(get_product_usecase),
):
    """Public endpoint to list all products."""
    return product_usecase.get_all_products()


@router.get("/category/{category_id}", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def get_products_by_category(
    category_id: UUID,
    product_usecase: ProductUsecase = Depends(get_product_usecase),
):
    """Public endpoint to list products by category."""
    return product_usecase.get_products_by_category(category_id)


@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product_by_id(
    product_id: UUID,
    product_usecase: ProductUsecase = Depends(get_product_usecase),
):
    """Public endpoint to retrieve a product by ID."""
    return product_usecase.get_product_by_id(product_id)


@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def update_product(
    product_id: UUID,
    product_request: ProductRequest,
    response: Response,
    _: AdminResponse = Depends(get_current_user),
    product_usecase: ProductUsecase = Depends(get_product_usecase),
):
    """Authenticated endpoint to update a product."""
    logger.info("Updating product", extra={"product_id": product_id})
    updated = product_usecase.update_product(product_id, product_request)
    response.headers["Location"] = f"{PRODUCT_PREFIX}/{product_id}"
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: UUID,
    _: AdminResponse = Depends(get_current_user),
    product_usecase: ProductUsecase = Depends(get_product_usecase),
):
    """Authenticated endpoint to delete a product."""
    logger.info("Deleting product", extra={"product_id": product_id})
    product_usecase.delete_product(product_id)
