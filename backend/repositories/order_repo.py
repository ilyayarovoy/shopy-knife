from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.database.models import OrderModel


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_orders(self, user_id: int):
        stmt = select(OrderModel).where(OrderModel.user_id == user_id).options(selectinload(OrderModel.user))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_order_by_id(self, order_id: int):
        stmt = select(OrderModel).where(OrderModel.id == order_id).options(selectinload(OrderModel.user))
        order = await self.session.execute(stmt)
        return order.scalar_one_or_none()

    async def create_order(self, user_id: int, total_price: float, status: str = "new"):
        new_order = OrderModel(user_id=user_id, total_price=total_price, status=status)
        self.session.add(new_order)
        await self.session.commit()
        await self.session.refresh(new_order)
        return new_order

    async def update_order_status(self, order: OrderModel, status: str):
        order.status = status
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order
