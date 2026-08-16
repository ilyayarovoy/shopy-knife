from pydantic import BaseModel, Field
from datetime import datetime


class UpdateOrderStatusSchema(BaseModel):
    status: str = Field(..., examples=["new", "processing", "completed", "cancelled"])


class OrderResponseSchema(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
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
