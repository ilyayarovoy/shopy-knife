from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from backend.database.engine import get_session
from backend.services.product_service import ProductService
from backend.api.schemas.product_schemas import CreateProductSchema

router = APIRouter(prefix="/products")
tags = ['Товары']

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_product_service(session: SessionDep) -> ProductService:
    return ProductService(session)


@router.get("/all", summary="Получить всех товары", tags=tags)
async def get_all_products(service: Annotated[ProductService, Depends(get_product_service)]):
    all_products = await service.get_all_products_service()
    if not all_products:
        raise HTTPException(status_code=404, detail="Not found products")
    return all_products

@router.get("/{product_id}", summary="Получить товар по ID", tags=tags)
async def get_product_by_tg_id(product_id: int, service: Annotated[ProductService, Depends(get_product_service)]):
    product = await service.get_product_by_id_service(product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Not found user by TG ID {}".format(product_id))
    return product_id

@router.post("", summary="Добавить товар", tags=tags, status_code=status.HTTP_201_CREATED)
async def create_product(new_product_data: CreateProductSchema, service: Annotated[ProductService, Depends(get_product_service)]):
    new_product = await service.create_new_product_service(product_data=new_product_data)
    return new_product


@router.delete("/{product_id}", summary="Удалить товар ID", tags=tags)
async def delete_product(product_id: int, service: Annotated[ProductService, Depends(get_product_service)]):
    product = await service.delete_product_by_id_service(product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Not found product by ID {}".format(product_id))
    return {"msg": "Product deleted successfully", "user": product}





