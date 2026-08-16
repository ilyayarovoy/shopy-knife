from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database.models import OrderItemModel


class OrderItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_items(self, order_id: int):
        stmt = select(OrderItemModel).where(OrderItemModel.order_id == order_id).options(selectinload(OrderItemModel.product))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_order_item_by_id(self, item_id: int):
        stmt = select(OrderItemModel).where(OrderItemModel.id == item_id).options(selectinload(OrderItemModel.product))
        item = await self.session.execute(stmt)
        return item.scalar_one_or_none()

    async def create_order_item(self, order_id: int, product_id: int, quantity: int, price_at_order: float):
        new_item = OrderItemModel(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price_at_order=price_at_order
        )
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        return new_item
