from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from backend.database.engine import get_session
from backend.services.favorite_service import FavoriteService
from backend.api.schemas.favorite_schemas import AddToFavoritesSchema, FavoriteItemResponseSchema, FavoritesResponseSchema, IsFavoriteResponseSchema

router = APIRouter(prefix="/favorites")
tags = ['Избранное']

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_favorite_service(session: SessionDep) -> FavoriteService:
    return FavoriteService(session)


@router.get("/user/{user_id}", summary="Получить список избранного пользователя", tags=tags, response_model=FavoritesResponseSchema)
async def get_user_favorites(
    user_id: int = Path(..., gt=0),
    service: Annotated[FavoriteService, Depends(get_favorite_service)] = None
):
    items = await service.get_user_favorites_service(user_id=user_id)
    return {
        "items": items,
        "total_count": len(items)
    }


@router.post("/user/{user_id}/add", summary="Добавить товар в избранное", tags=tags, status_code=status.HTTP_201_CREATED, response_model=FavoriteItemResponseSchema)
async def add_to_favorites(
    user_id: int = Path(..., gt=0),
    favorite_data: AddToFavoritesSchema = None,
    service: Annotated[FavoriteService, Depends(get_favorite_service)] = None
):
    result = await service.add_to_favorites_service(user_id=user_id, product_id=favorite_data.product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


@router.delete("/user/{user_id}/item/{item_id}", summary="Удалить товар из избранного", tags=tags, status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_favorites(
    user_id: int = Path(..., gt=0),
    item_id: int = Path(..., gt=0),
    service: Annotated[FavoriteService, Depends(get_favorite_service)] = None
):
    item = await service.remove_from_favorites_service(item_id=item_id, user_id=user_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Favorite item not found")
    if isinstance(item, dict) and "error" in item:
        raise HTTPException(status_code=403, detail=item["error"])


@router.get("/user/{user_id}/check/{product_id}", summary="Проверить, находится ли товар в избранном", tags=tags, response_model=IsFavoriteResponseSchema)
async def is_product_favorite(
    user_id: int = Path(..., gt=0),
    product_id: int = Path(..., gt=0),
    service: Annotated[FavoriteService, Depends(get_favorite_service)] = None
):
    is_favorite = await service.is_favorite_service(user_id=user_id, product_id=product_id)
    return {"is_favorite": is_favorite}
