from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.cart_repo import CartRepository
from backend.repositories.product_repo import ProductRepository


class CartService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.cart_repo = CartRepository(session=self.session)
        self.product_repo = ProductRepository(session=self.session)

    async def get_user_cart_service(self, user_id: int):
        items = await self.cart_repo.get_user_cart(user_id=user_id)
        result = []
        for item in items:
            result.append({
                "id": item.id,
                "user_id": item.user_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
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

    async def add_to_cart_service(self, user_id: int, product_id: int, quantity: int = 1):
        product = await self.product_repo.get_product_by_id(product_id=product_id)
        if not product:
            return None

        if product.stock < quantity:
            return {"error": "Not enough stock"}

        item = await self.cart_repo.add_to_cart(user_id=user_id, product_id=product_id, quantity=quantity)
        return {
            "id": item.id,
            "user_id": item.user_id,
            "product_id": item.product_id,
            "quantity": item.quantity,
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

    async def update_cart_item_service(self, item_id: int, user_id: int, quantity: int):
        item = await self.cart_repo.get_cart_item_by_id(item_id=item_id)
        if not item:
            return None

        if item.user_id != user_id:
            return {"error": "Forbidden: Item does not belong to this user", "status_code": 403}

        if item.product.stock < quantity:
            return {"error": "Not enough stock"}

        updated_item = await self.cart_repo.update_cart_item(item=item, quantity=quantity)
        return {
            "id": updated_item.id,
            "user_id": updated_item.user_id,
            "product_id": updated_item.product_id,
            "quantity": updated_item.quantity,
            "product": {
                "id": updated_item.product.id,
                "category_id": updated_item.product.category_id,
                "title": updated_item.product.title,
                "price": updated_item.product.price,
                "description": updated_item.product.description,
                "images": updated_item.product.images
            },
            "created_at": updated_item.created_at
        }

    async def remove_from_cart_service(self, item_id: int, user_id: int):
        item = await self.cart_repo.get_cart_item_by_id(item_id=item_id)
        if not item:
            return None

        if item.user_id != user_id:
            return {"error": "Forbidden: Item does not belong to this user"}

        await self.cart_repo.remove_from_cart(item=item)
        return item

    async def clear_cart_service(self, user_id: int):
        await self.cart_repo.clear_user_cart(user_id=user_id)
        return {"message": "Cart cleared"}
