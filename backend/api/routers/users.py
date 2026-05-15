from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from backend.database.engine import get_session
from backend.services.user_service import UserService
from backend.api.schemas.users_schemas import CreateUserSchema

router = APIRouter(prefix="/users")
tags = ['Пользователи']

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)


@router.get("", summary="Получить всех пользователей приложения", tags=tags)
async def get_all_users(service: Annotated[UserService, Depends(get_user_service)]):
    all_users = await service.get_all_users_service()
    if not all_users:
        raise HTTPException(status_code=404, detail="Not found users")
    return all_users

@router.get("/{tg_id}", summary="Получить пользователя по TG_ID", tags=tags)
async def get_user_by_tg_id(tg_id: int, service: Annotated[UserService, Depends(get_user_service)]):
    user = await service.get_user_by_tg_id_service(tg_id=tg_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not found user by TG ID {}".format(tg_id))
    return user

@router.get("", summary="Добавить пользователя", tags=tags)
async def create_user(new_user_data: CreateUserSchema, service: Annotated[UserService, Depends(get_user_service)])
    new_user = await service.create_new_user_service(user=new_user_data)
    user = new_user.username or new_user.tg_id
    return {"msg": "User created successfully", "user": user}





