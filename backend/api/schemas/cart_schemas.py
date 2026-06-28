from pydantic import BaseModel, Field
from datetime import datetime


class AddToCartSchema(BaseModel):
    product_id: int = Field(examples=[1])
    quantity: int = Field(default=1, ge=1, examples=[1])


class UpdateCartItemSchema(BaseModel):
    quantity: int = Field(ge=1, examples=[2])


class CartItemProductSchema(BaseModel):
    id: int
    title: str
    price: float
    description: str | None
    images: list[str] | None

    class Config:
        from_attributes = True


class CartItemResponseSchema(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    product: CartItemProductSchema
    created_at: datetime

    class Config:
        from_attributes = True


class CartResponseSchema(BaseModel):
    items: list[CartItemResponseSchema]
    total_items: int
    total_price: float

    class Config:
        from_attributes = True
