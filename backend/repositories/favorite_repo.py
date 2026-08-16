from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database.models import FavoriteModel


class FavoriteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_favorites(self, user_id: int):
        stmt = select(FavoriteModel).where(FavoriteModel.user_id == user_id).options(selectinload(FavoriteModel.product))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_favorite_by_id(self, favorite_id: int):
        stmt = select(FavoriteModel).where(FavoriteModel.id == favorite_id).options(selectinload(FavoriteModel.product))
        item = await self.session.execute(stmt)
        return item.scalar_one_or_none()

    async def get_favorite_by_user_and_product(self, user_id: int, product_id: int):
        stmt = select(FavoriteModel).where(
            (FavoriteModel.user_id == user_id) & (FavoriteModel.product_id == product_id)
        ).options(selectinload(FavoriteModel.product))
        item = await self.session.execute(stmt)
        return item.scalar_one_or_none()

    async def add_to_favorites(self, user_id: int, product_id: int):
        existing_item = await self.get_favorite_by_user_and_product(user_id, product_id)
        if existing_item:
            return existing_item

        new_item = FavoriteModel(user_id=user_id, product_id=product_id)
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        return new_item

    async def remove_from_favorites(self, item: FavoriteModel):
        await self.session.delete(item)
        await self.session.commit()

    async def is_favorite(self, user_id: int, product_id: int) -> bool:
        item = await self.get_favorite_by_user_and_product(user_id, product_id)
        return item is not None
