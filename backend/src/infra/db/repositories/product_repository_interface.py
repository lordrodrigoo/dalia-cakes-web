from uuid import UUID
from typing import Optional
from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.infra.db.entities.product import ProductEntity
from backend.src.domain.repositories.product_repository import ProductRepositoryInterface
from backend.src.domain.models.product import Product


class ProductRepository(ProductRepositoryInterface):
    def __init__(self, db_connection: DBConnectionHandler):
        self.session = db_connection.get_session()

    def create_product(self, product: Product) -> Product:
        entity = ProductEntity(
            name=product.name,
            price=product.price,
            image_url=product.image_url,
            category_id=product.category_id,
        )
        self.session.add(entity)
        self.session.flush()
        return Product.from_entity(entity)

    def update_product(self, product: Product) -> Product:
        entity = self.session.query(ProductEntity).filter_by(id=product.id).first()
        if entity:
            entity.name = product.name
            entity.price = product.price
            entity.image_url = product.image_url
            entity.category_id = product.category_id
            self.session.flush()
            return Product.from_entity(entity)
        return None

    def delete_product(self, product_id: UUID) -> None:
        self.session.query(ProductEntity).filter_by(id=product_id).delete()

    def get_product_by_id(self, product_id: UUID) -> Optional[Product]:
        entity = self.session.query(ProductEntity).filter_by(id=product_id).first()
        return Product.from_entity(entity) if entity else None

    def get_all_products(self) -> list[Product]:
        entities = self.session.query(ProductEntity).all()
        return [Product.from_entity(e) for e in entities]

    def get_products_by_category(self, category_id: UUID) -> list[Product]:
        entities = self.session.query(ProductEntity).filter_by(category_id=category_id).all()
        return [Product.from_entity(e) for e in entities]
