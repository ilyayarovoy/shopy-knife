from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.order_repo import OrderRepository
from backend.repositories.order_item_repo import OrderItemRepository
from backend.repositories.cart_repo import CartRepository
from backend.repositories.product_repo import ProductRepository


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session=self.session)
        self.order_item_repo = OrderItemRepository(session=self.session)
        self.cart_repo = CartRepository(session=self.session)
        self.product_repo = ProductRepository(session=self.session)

    async def get_user_orders_service(self, user_id: int):
        orders = await self.order_repo.get_user_orders(user_id=user_id)
        result = []
        for order in orders:
            result.append({
                "id": order.id,
                "user_id": order.user_id,
                "total_price": order.total_price,
                "status": order.status,
                "created_at": order.created_at
            })
        return result

    async def checkout_service(self, user_id: int):
        # Get all cart items for user
        cart_items = await self.cart_repo.get_user_cart(user_id=user_id)

        if not cart_items:
            return {"error": "Cart is empty"}

        # Calculate total price and validate stock
        total_price = 0
        for item in cart_items:
            product = item.product
            if product.stock < item.quantity:
                return {"error": f"Not enough stock for {product.title}"}
            total_price += float(product.price) * item.quantity

        # Create order
        order = await self.order_repo.create_order(user_id=user_id, total_price=total_price, status="new")

        # Create order items and update product stock
        for item in cart_items:
            product = item.product
            # Create order item with price snapshot
            await self.order_item_repo.create_order_item(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                price_at_order=float(product.price)
            )
            # Update product stock
            new_stock = product.stock - item.quantity
            await self.product_repo.update_product(product=product, stock=new_stock)

        # Clear cart
        await self.cart_repo.clear_user_cart(user_id=user_id)

        return {
            "id": order.id,
            "user_id": order.user_id,
            "total_price": order.total_price,
            "status": order.status,
            "created_at": order.created_at
        }

    async def get_order_by_id_service(self, order_id: int):
        order = await self.order_repo.get_order_by_id(order_id=order_id)
        if not order:
            return None

        # Get order items
        items = await self.order_item_repo.get_order_items(order_id=order_id)

        items_data = []
        for item in items:
            items_data.append({
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_at_order": item.price_at_order,
                "product": {
                    "id": item.product.id,
                    "category_id": item.product.category_id,
                    "title": item.product.title,
                    "price": item.product.price,
                    "description": item.product.description,
                    "images": item.product.images
                }
            })

        return {
            "id": order.id,
            "user_id": order.user_id,
            "total_price": order.total_price,
            "status": order.status,
            "items": items_data,
            "created_at": order.created_at
        }

    async def update_order_status_service(self, order_id: int, new_status: str, user_id: int | None = None):
        order = await self.order_repo.get_order_by_id(order_id=order_id)
        if not order:
            return None

        # Пропустить проверку владельца если user_id=None (для bot callback)
        if user_id is not None and order.user_id != user_id:
            return {"error": "Forbidden: Order does not belong to this user"}

        updated_order = await self.order_repo.update_order_status(order=order, status=new_status)
        return {
            "id": updated_order.id,
            "user_id": updated_order.user_id,
            "total_price": updated_order.total_price,
            "status": updated_order.status,
            "created_at": updated_order.created_at
        }

    async def delete_order_service(self, order_id: int, user_id: int):
        order = await self.order_repo.get_order_by_id(order_id=order_id)
        if not order:
            return None

        if order.user_id != user_id:
            return {"error": "Forbidden: Order does not belong to this user"}

        if order.status != "new":
            return {"error": f"Cannot delete order with status '{order.status}'. Only 'new' orders can be deleted."}

        # Return stock to products
        items = await self.order_item_repo.get_order_items(order_id=order_id)
        for item in items:
            product = item.product
            new_stock = product.stock + item.quantity
            await self.product_repo.update_product(product=product, stock=new_stock)

        # Delete order (order_items will be deleted by CASCADE)
        await self.order_repo.delete_order(order=order)
        return {"message": "Order deleted successfully"}
