from pydantic import BaseModel, Field, field_validator


class CreateProductSchema(BaseModel):
    title: str = Field(examples=["Баварский клин"])
    description: str | None = Field(default=None, examples=['Описание...'])
    price: float = Field(gt=0, examples=[1299.99])
    stock: int = Field(ge=0, examples=[10])
    images: list[str] | None = Field(default=None, examples=[
        "https://res.cloudinary.com/demo/image/upload/v1/photo1.jpg",
        "https://res.cloudinary.com/demo/image/upload/v2/photo2.jpg"
    ])


class UpdateProductSchema(BaseModel):
    title: str | None = Field(default=None, examples=["Баварский клин"])
    description: str | None = Field(default=None, examples=['Описание...'])
    price: float | None = Field(default=None, gt=0, examples=[1299.99])
    stock: int | None = Field(default=None, ge=0, examples=[10])
    images: list[str] | None = Field(default=None, examples=[
        "https://res.cloudinary.com/demo/image/upload/v1/photo1.jpg",
        "https://res.cloudinary.com/demo/image/upload/v2/photo2.jpg"
    ])


class ProductResponseSchema(BaseModel):
    id: int
    title: str
    description: str | None
    price: float
    stock: int
    images: list[str] | None

    class Config:
        from_attributes = True

