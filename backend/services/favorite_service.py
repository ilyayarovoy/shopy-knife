from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.favorite_repo import FavoriteRepository
from backend.repositories.product_repo import ProductRepository


class FavoriteService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.favorite_repo = FavoriteRepository(session=self.session)
        self.product_repo = ProductRepository(session=self.session)

    async def get_user_favorites_service(self, user_id: int):
        items = await self.favorite_repo.get_user_favorites(user_id=user_id)
        result = []
        for item in items:
            result.append({
                "id": item.id,
                "user_id": item.user_id,
                "product_id": item.product_id,
                "product": {
                    "id": item.product.id,
                    "category_id": item.product.category_id,
                    "title": item.product.title,
                    "price": item.product.price,
                    "description": item.product.description,
                    "images": item.product.images
                },
                "created_at": item.created_at
            })
        return result

    async def add_to_favorites_service(self, user_id: int, product_id: int):
        product = await self.product_repo.get_product_by_id(product_id=product_id)
        if not product:
            return None

        item = await self.favorite_repo.add_to_favorites(user_id=user_id, product_id=product_id)
        return {
            "id": item.id,
            "user_id": item.user_id,
            "product_id": item.product_id,
            "product": {
                "id": item.product.id,
                "category_id": item.product.category_id,
                "title": item.product.title,
                "price": item.product.price,
                "description": item.product.description,
                "images": item.product.images
            },
            "created_at": item.created_at
        }

    async def remove_from_favorites_service(self, item_id: int, user_id: int):
        item = await self.favorite_repo.get_favorite_by_id(item_id=item_id)
        if not item:
            return None

        if item.user_id != user_id:
            return {"error": "Forbidden: Item does not belong to this user"}

        await self.favorite_repo.remove_from_favorites(item=item)
        return item

    async def is_favorite_service(self, user_id: int, product_id: int) -> bool:
        return await self.favorite_repo.is_favorite(user_id=user_id, product_id=product_id)
