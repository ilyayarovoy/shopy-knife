from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import CartItemModel


class CartRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_cart(self, user_id: int):
        stmt = select(CartItemModel).where(CartItemModel.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_cart_item_by_id(self, item_id: int):
        stmt = select(CartItemModel).where(CartItemModel.id == item_id)
        item = await self.session.execute(stmt)
        return item.scalar_one_or_none()

    async def get_cart_item_by_user_and_product(self, user_id: int, product_id: int):
        stmt = select(CartItemModel).where(
            (CartItemModel.user_id == user_id) & (CartItemModel.product_id == product_id)
        )
        item = await self.session.execute(stmt)
        return item.scalar_one_or_none()

    async def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1):
        existing_item = await self.get_cart_item_by_user_and_product(user_id, product_id)

        if existing_item:
            existing_item.quantity += quantity
            self.session.add(existing_item)
            await self.session.commit()
            await self.session.refresh(existing_item)
            return existing_item

        new_item = CartItemModel(user_id=user_id, product_id=product_id, quantity=quantity)
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        return new_item

    async def update_cart_item(self, item: CartItemModel, quantity: int):
        item.quantity = quantity
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def remove_from_cart(self, item: CartItemModel):
        await self.session.delete(item)
        await self.session.commit()

    async def clear_user_cart(self, user_id: int):
        stmt = select(CartItemModel).where(CartItemModel.user_id == user_id)
        result = await self.session.execute(stmt)
        items = result.scalars().all()
        for item in items:
            await self.session.delete(item)
        await self.session.commit()
