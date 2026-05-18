from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import ProductModel

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all_products(self):
        stmt = select(ProductModel)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_product_by_id(self, product_id: int):
        stmt = select(ProductModel).where(ProductModel.id == product_id)
        product = await self.session.execute(stmt)
        return product.scalar_one_or_none()


    async def create_product(self,
                          title: str,
                          description: str,
                          price: float,
                          stock: int,
                             image_url: str,):
        new_product = ProductModel(title=title,
                             description=description,
                             price=price,
                             stock=stock,
                             image_url=image_url
                                   )


        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product


    async def delete_product(self, product):
        await self.session.delete(product)
        await self.session.commit()
        return product


