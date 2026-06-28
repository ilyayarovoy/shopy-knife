from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from backend.database.engine import get_session
from backend.services.category_service import CategoryService
from backend.api.schemas.category_schemas import CreateCategorySchema, UpdateCategorySchema, CategoryResponseSchema

router = APIRouter(prefix="/categories")
tags = ['Категории']

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_category_service(session: SessionDep) -> CategoryService:
    return CategoryService(session)


@router.get("/all", summary="Получить все категории", tags=tags, response_model=list[CategoryResponseSchema])
async def get_all_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    service: Annotated[CategoryService, Depends(get_category_service)] = None
):
    categories = await service.get_all_categories_service(skip=skip, limit=limit)
    if not categories:
        raise HTTPException(status_code=404, detail="Category not found")
    return categories



@router.get("/{category_id}", summary="Получить категорию по ID", tags=tags, response_model=CategoryResponseSchema)
async def get_category_by_id(
    category_id: int,
    service: Annotated[CategoryService, Depends(get_category_service)] = None
):
    category = await service.get_category_by_id_service(category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("", summary="Создать категорию", tags=tags, status_code=status.HTTP_201_CREATED, response_model=CategoryResponseSchema)
async def create_category(
    category_data: CreateCategorySchema,
    service: Annotated[CategoryService, Depends(get_category_service)] = None
):
    new_category = await service.create_category_service(category_data=category_data)
    return new_category


@router.put("/{category_id}", summary="Обновить категорию", tags=tags, response_model=CategoryResponseSchema)
async def update_category(
    category_id: int,
    category_data: UpdateCategorySchema,
    service: Annotated[CategoryService, Depends(get_category_service)] = None
):
    updated_category = await service.update_category_service(category_id=category_id, category_data=category_data)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category


@router.delete("/{category_id}", summary="Удалить категорию", tags=tags)
async def delete_category(
    category_id: int,
    service: Annotated[CategoryService, Depends(get_category_service)] = None
):
    category = await service.delete_category_service(category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"msg": "Category deleted successfully", "category": category}
