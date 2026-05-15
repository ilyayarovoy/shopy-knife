from pydantic import BaseModel, Field


class CreateUserSchema(BaseModel):
    tg_id: int
    username: str | None = Field(default=None, examples=['@Avarde808'])
    firstname: str | None = Field(default=None, examples=['Илья'])
    lastname: str | None = Field(default=None, examples=['Пономорев'])