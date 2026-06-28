from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import CategoryModel


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_categories(self, skip: int = 0, limit: int = 100):
        stmt = select(CategoryModel).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_category_by_id(self, category_id: int):
        stmt = select(CategoryModel).where(CategoryModel.id == category_id)
        category = await self.session.execute(stmt)
        return category.scalar_one_or_none()

    async def get_category_by_slug(self, slug: str):
        stmt = select(CategoryModel).where(CategoryModel.slug == slug)
        category = await self.session.execute(stmt)
        return category.scalar_one_or_none()

    async def create_category(self, name: str, description: str | None, slug: str):
        new_category = CategoryModel(name=name, description=description, slug=slug)
        self.session.add(new_category)
        await self.session.commit()
        await self.session.refresh(new_category)
        return new_category

    async def update_category(self, category: CategoryModel, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(category, key, value)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def delete_category(self, category: CategoryModel):
        await self.session.delete(category)
        await self.session.commit()
        return category
