from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.category_repo import CategoryRepository
from backend.api.schemas.category_schemas import CreateCategorySchema, UpdateCategorySchema


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.category_repo = CategoryRepository(session=self.session)

    async def get_all_categories_service(self, skip: int = 0, limit: int = 100):
        categories = await self.category_repo.get_all_categories(skip=skip, limit=limit)
        return [
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "slug": category.slug,
                "created_at": category.created_at
            }
            for category in categories
        ]

    async def get_category_by_id_service(self, category_id: int):
        category = await self.category_repo.get_category_by_id(category_id=category_id)
        return category

    async def create_category_service(self, category_data: CreateCategorySchema):
        new_category = await self.category_repo.create_category(
            name=category_data.name,
            description=category_data.description,
            slug=category_data.slug
        )
        return new_category

    async def update_category_service(self, category_id: int, category_data: UpdateCategorySchema):
        category = await self.category_repo.get_category_by_id(category_id=category_id)
        if not category:
            return None

        updated_category = await self.category_repo.update_category(
            category,
            name=category_data.name,
            description=category_data.description,
            slug=category_data.slug
        )
        return updated_category

    async def delete_category_service(self, category_id: int):
        category = await self.category_repo.get_category_by_id(category_id=category_id)
        if category:
            await self.category_repo.delete_category(category=category)
        return category
