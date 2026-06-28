from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import ProductModel

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_all_products(self, skip: int = 0, limit: int = 100, title: str | None = None, category_id: int | None = None, min_price: float | None = None, max_price: float | None = None):
        stmt = select(ProductModel)

        if title:
            stmt = stmt.where(ProductModel.title.ilike(f"%{title}%"))
        if category_id is not None:
            stmt = stmt.where(ProductModel.category_id == category_id)
        if min_price is not None:
            stmt = stmt.where(ProductModel.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(ProductModel.price <= max_price)

        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_product_by_id(self, product_id: int):
        stmt = select(ProductModel).where(ProductModel.id == product_id)
        product = await self.session.execute(stmt)
        return product.scalar_one_or_none()


    async def create_product(self,
                          category_id: int,
                          title: str,
                          description: str,
                          price: float,
                          stock: int,
                          images: list[str] | None = None,):
        new_product = ProductModel(category_id=category_id,
                             title=title,
                             description=description,
                             price=price,
                             stock=stock,
                             images=images
                                   )


        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product

    async def update_product(self, product: ProductModel, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(product, key, value)

        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete_product(self, product):
        await self.session.delete(product)
        await self.session.commit()
        return product


