from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.product_repo import ProductRepository
from backend.repositories.category_repo import CategoryRepository
from backend.api.schemas.product_schemas import CreateProductSchema, UpdateProductSchema


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.product_repo = ProductRepository(session=self.session)
        self.category_repo = CategoryRepository(session=self.session)


    async def get_all_products_service(self, skip: int = 0, limit: int = 100, title: str | None = None, category_id: int | None = None, min_price: float | None = None, max_price: float | None = None):
        products = await self.product_repo.get_all_products(skip=skip, limit=limit, title=title, category_id=category_id, min_price=min_price, max_price=max_price)
        return [
            {
                "id": product.id,
                "category_id": product.category_id,
                "title": product.title,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "images": product.images
            }
            for product in products
        ]


    async def get_product_by_id_service(self, product_id: int):
        product = await self.product_repo.get_product_by_id(product_id=product_id)
        return product

    async def create_new_product_service(self, product_data: CreateProductSchema):
        category = await self.category_repo.get_category_by_id(product_data.category_id)
        if not category:
            return {"error": f"Category with id {product_data.category_id} not found"}

        new_product = await self.product_repo.create_product(
            category_id=product_data.category_id,
            title=product_data.title,
            description=product_data.description,
            price=product_data.price,
            stock=product_data.stock,
            images=product_data.images
        )
        return new_product

    async def update_product_service(self, product_id: int, product_data: UpdateProductSchema):
        product = await self.product_repo.get_product_by_id(product_id=product_id)
        if not product:
            return None

        if product_data.category_id:
            category = await self.category_repo.get_category_by_id(product_data.category_id)
            if not category:
                return {"error": f"Category with id {product_data.category_id} not found"}

        updated_product = await self.product_repo.update_product(
            product,
            category_id=product_data.category_id,
            title=product_data.title,
            description=product_data.description,
            price=product_data.price,
            stock=product_data.stock,
            images=product_data.images
        )
        return updated_product

    async def delete_product_by_id_service(self, product_id: int):
        product = await self.product_repo.get_product_by_id(product_id=product_id)
        if product:
            await self.product_repo.delete_product(product=product)
        return product
