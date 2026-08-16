from pydantic import BaseModel, Field
from datetime import datetime


class UpdateOrderStatusSchema(BaseModel):
    status: str = Field(..., examples=["new", "processing", "completed", "cancelled"])


class OrderItemProductSchema(BaseModel):
    id: int
    category_id: int
    title: str
    price: float
    description: str | None
    images: list[str] | None

    class Config:
        from_attributes = True


class OrderItemResponseSchema(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_order: float
    product: OrderItemProductSchema

    class Config:
        from_attributes = True


class OrderResponseSchema(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    items: list[OrderItemResponseSchema] | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class OrdersListResponseSchema(BaseModel):
    items: list[OrderResponseSchema]
    total_count: int

    class Config:
        from_attributes = True


class CheckoutResponseSchema(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
