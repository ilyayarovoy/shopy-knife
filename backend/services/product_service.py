from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.product_repo import ProductRepository
from backend.api.schemas.product_schemas import CreateProductSchema, UpdateProductSchema


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.product_repo = ProductRepository(session=self.session)


    async def get_all_products_service(self, skip: int = 0, limit: int = 100, title: str | None = None, min_price: float | None = None, max_price: float | None = None):
        products = await self.product_repo.get_all_products(skip=skip, limit=limit, title=title, min_price=min_price, max_price=max_price)
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
