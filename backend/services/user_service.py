from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.user_repo import UserRepository
from backend.api.schemas.users_schemas import CreateUserSchema


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.user_repo = UserRepository(session=self.session)


    async def get_all_users_service(self):
        our_users = await self.user_repo.get_all_users()
        return [
            {
                "id": user.id,
                "tg_id": user.tg_id,
                "username": user.username,
                "created_at": user.created_at
            }
            for user in our_users
        ]

    async def get_user_by_tg_id_service(self, tg_id):
        user = await self.user_repo.get_user_by_tg_id(tg_id=tg_id)
        return user


    async def create_new_user_service(self, user: CreateUserSchema):
        existing_user = await self.user_repo.get_user_by_tg_id(tg_id=user.tg_id)
        if existing_user:
            return existing_user
        else:
            new_user = await self.user_repo.create_user(
                tg_id=user.tg_id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            return new_user
