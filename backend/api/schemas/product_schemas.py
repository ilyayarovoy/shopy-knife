from pydantic import BaseModel, Field


class CreateProductSchema(BaseModel):
    title: str = Field(examples=["Баварский клин"])
    description: str | None = Field(default=None, examples=['Описание...'])
    price: float | None = Field(default=0.0)
    stock: int | None = Field(default=0)
    images: list[str] | None = Field(default=None, examples=[
        "https://res.cloudinary.com/demo/image/upload/v1/photo1.jpg",
        "https://res.cloudinary.com/demo/image/upload/v2/photo2.jpg"
    ])

