from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from backend.database.engine import get_session


router = APIRouter(prefix="/products")
tags = ['Продукты']

SessionDep = Annotated[AsyncSession, Depends(get_session)]



@router.get("", summary="Получить всех пользователей", tags=tags)
async def get_all_products():
    return {"msg": "all products"}


