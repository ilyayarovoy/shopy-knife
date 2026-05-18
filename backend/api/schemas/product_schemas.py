from pydantic import BaseModel, Field


class CreateProductSchema(BaseModel):
    title: str = Field(examples=["Баварский клин"])
    description: str | None = Field(default=None, examples=['Описание...'])
    price: float | None = Field(default=0.0)
    stock: int | None = Field(default=0)
    image_url: str | None = Field(default=None)

