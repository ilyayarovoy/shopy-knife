from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from backend.database.engine import get_session
from backend.services.cart_service import CartService
from backend.api.schemas.cart_schemas import AddToCartSchema, UpdateCartItemSchema, CartItemResponseSchema, CartResponseSchema

router = APIRouter(prefix="/cart")
tags = ['Корзина']

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_cart_service(session: SessionDep) -> CartService:
    return CartService(session)


@router.get("/user/{user_id}", summary="Получить корзину пользователя", tags=tags, response_model=CartResponseSchema)
async def get_user_cart(
    user_id: int = Path(..., gt=0),
    service: Annotated[CartService, Depends(get_cart_service)] = None
):
    items = await service.get_user_cart_service(user_id=user_id)
    total_items = sum(item["quantity"] for item in items)
    total_price = sum(item["quantity"] * item["product"]["price"] for item in items)
    return {
        "items": items,
        "total_items": total_items,
        "total_price": total_price
    }


@router.post("/user/{user_id}/add", summary="Добавить товар в корзину", tags=tags, status_code=status.HTTP_201_CREATED, response_model=CartItemResponseSchema)
async def add_to_cart(
    user_id: int = Path(..., gt=0),
    cart_data: AddToCartSchema = None,
    service: Annotated[CartService, Depends(get_cart_service)] = None
):
    result = await service.add_to_cart_service(user_id=user_id, product_id=cart_data.product_id, quantity=cart_data.quantity)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.put("/item/{item_id}", summary="Обновить количество товара в корзине", tags=tags, response_model=CartItemResponseSchema)
async def update_cart_item(
    item_id: int = Path(..., gt=0),
    update_data: UpdateCartItemSchema = None,
    service: Annotated[CartService, Depends(get_cart_service)] = None
):
    result = await service.update_cart_item_service(item_id=item_id, quantity=update_data.quantity)
    if result is None:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.delete("/item/{item_id}", summary="Удалить товар из корзины", tags=tags)
async def remove_from_cart(
    item_id: int = Path(..., gt=0),
    service: Annotated[CartService, Depends(get_cart_service)] = None
):
    item = await service.remove_from_cart_service(item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"msg": "Item removed from cart successfully"}


@router.delete("/user/{user_id}/clear", summary="Очистить корзину пользователя", tags=tags)
async def clear_user_cart(
    user_id: int = Path(..., gt=0),
    service: Annotated[CartService, Depends(get_cart_service)] = None
):
    result = await service.clear_cart_service(user_id=user_id)
    return result
