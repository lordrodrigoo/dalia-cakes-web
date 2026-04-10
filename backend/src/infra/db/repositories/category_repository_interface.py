from uuid import UUID
from typing import Optional
from backend.src.infra.db.settings.connection import DBConnectionHandler
from backend.src.infra.db.entities.category import CategoryEntity
from backend.src.domain.repositories.category_repository import CategoryRepositoryInterface
from backend.src.domain.models.category import Category

class CategoryRepository(CategoryRepositoryInterface):
    def __init__(self, db_connection: DBConnectionHandler):
        self.session = db_connection.get_session()

    def create_category(self, category: Category) -> Category:
        entity = CategoryEntity(
            name=category.name,
            slug=category.slug,
            image_url=category.image_url,
        )
        self.session.add(entity)
        self.session.flush()
        return Category.from_entity(entity)

    def update_category(self, category: Category) -> Category:
        entity = self.session.query(CategoryEntity).filter_by(id=category.id).first()
        if entity:
            entity.name = category.name
            entity.slug = category.slug
            entity.image_url = category.image_url
            self.session.flush()
            return Category.from_entity(entity)
        return None

    def delete_category(self, category_id: UUID) -> None:
        self.session.query(CategoryEntity).filter_by(id=category_id).delete()

    def get_category_by_id(self, category_id: UUID) -> Optional[Category]:
        entity = self.session.query(CategoryEntity).filter_by(id=category_id).first()
        return Category.from_entity(entity) if entity else None

    def get_category_by_slug(self, slug: str) -> Optional[Category]:
        entity = self.session.query(CategoryEntity).filter_by(slug=slug).first()
        return Category.from_entity(entity) if entity else None

    def get_all_categories(self) -> list[Category]:
        entities = self.session.query(CategoryEntity).all()
        return [Category.from_entity(e) for e in entities]

    def get_category_by_name(self, name: str) -> Optional[Category]:
        entity = self.session.query(CategoryEntity).filter_by(name=name).first()
        return Category.from_entity(entity) if entity else None
