from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.product_repo import ProductRepository
from backend.api.schemas.product_schemas import CreateProductSchema


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.product_repo = ProductRepository(session=self.session)


    async def get_all_products_service(self):
        products = await self.product_repo.get_all_products()
        return [
            {
                "id": product.id,
                "title": products.title,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "image_url": product.image_url
            }
            for product in products
        ]


    async def get_product_by_id_service(self, product_id: int):
        product = await self.product_repo.get_product_by_id(product_id=product_id)
        return product


    async def create_new_product_service(self, product_data: CreateProductSchema):
        existing_products = await self.product_repo.get_product_by_id(product_id=product_data.id)
        if existing_products:
            return existing_products
        else:
            new_product = await self.product_repo.create_product(
                title=product_data.title,
                description=product_data.description,
                price=product_data.stock,
                stock=product_data.stock,
                image_url=product_data.image_url
            )
            return new_product

    async def delete_product_by_id_service(self, product_id: int):
        product = await self.product_repo.get_product_by_id(product_id=product_id)
        if product:
            await self.product_repo.delete_product(product=product)
        return product
