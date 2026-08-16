from pydantic import BaseModel, Field
from datetime import datetime


class AddToFavoritesSchema(BaseModel):
    product_id: int = Field(examples=[1])


class FavoriteItemProductSchema(BaseModel):
    id: int
    category_id: int
    title: str
    price: float
    description: str | None
    images: list[str] | None

    class Config:
        from_attributes = True


class FavoriteItemResponseSchema(BaseModel):
    id: int
    user_id: int
    product_id: int
    product: FavoriteItemProductSchema
    created_at: datetime

    class Config:
        from_attributes = True


class FavoritesResponseSchema(BaseModel):
    items: list[FavoriteItemResponseSchema]
    total_count: int

    class Config:
        from_attributes = True


class IsFavoriteResponseSchema(BaseModel):
    is_favorite: bool
