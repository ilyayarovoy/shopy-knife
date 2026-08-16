from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from backend.database.engine import get_session
from backend.services.order_service import OrderService
from backend.api.schemas.order_schemas import (
    UpdateOrderStatusSchema,
    OrderResponseSchema,
    OrdersListResponseSchema,
    CheckoutResponseSchema
)

router = APIRouter(prefix="/orders")
tags = ['Заказы']

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_order_service(session: SessionDep) -> OrderService:
    return OrderService(session)


@router.post("/user/{user_id}/checkout", summary="Оформить заказ", tags=tags, status_code=status.HTTP_201_CREATED, response_model=CheckoutResponseSchema)
async def checkout(
    user_id: int = Path(..., gt=0),
    service: Annotated[OrderService, Depends(get_order_service)] = None
):
    result = await service.checkout_service(user_id=user_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/user/{user_id}", summary="Получить заказы пользователя", tags=tags, response_model=OrdersListResponseSchema)
async def get_user_orders(
    user_id: int = Path(..., gt=0),
    service: Annotated[OrderService, Depends(get_order_service)] = None
):
    orders = await service.get_user_orders_service(user_id=user_id)
    return {
        "items": orders,
        "total_count": len(orders)
    }


@router.get("/{order_id}", summary="Получить заказ по ID", tags=tags, response_model=OrderResponseSchema)
async def get_order_by_id(
    order_id: int = Path(..., gt=0),
    service: Annotated[OrderService, Depends(get_order_service)] = None
):
    order = await service.get_order_by_id_service(order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}/user/{user_id}/status", summary="Обновить статус заказа", tags=tags, response_model=OrderResponseSchema)
async def update_order_status(
    order_id: int = Path(..., gt=0),
    user_id: int = Path(..., gt=0),
    status_data: UpdateOrderStatusSchema = None,
    service: Annotated[OrderService, Depends(get_order_service)] = None
):
    result = await service.update_order_status_service(order_id=order_id, new_status=status_data.status, user_id=user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=403, detail=result["error"])
    return result
