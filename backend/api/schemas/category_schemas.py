from pydantic import BaseModel, Field
from datetime import datetime


class CreateCategorySchema(BaseModel):
    name: str = Field(examples=["Кухонные ножи"])
    description: str | None = Field(default=None, examples=["Профессиональные ножи для кухни"])
    slug: str = Field(examples=["kitchen-knives"])


class UpdateCategorySchema(BaseModel):
    name: str | None = Field(default=None, examples=["Кухонные ножи"])
    description: str | None = Field(default=None, examples=["Профессиональные ножи для кухни"])
    slug: str | None = Field(default=None, examples=["kitchen-knives"])


class CategoryResponseSchema(BaseModel):
    id: int
    name: str
    description: str | None
    slug: str
    created_at: datetime

    class Config:
        from_attributes = True
