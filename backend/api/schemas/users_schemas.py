from pydantic import BaseModel, Field


class CreateUserSchema(BaseModel):
    tg_id: int
    username: str | None = Field(default=None, examples=['@Avarde808'])
    first_name: str | None = Field(default=None, examples=['Илья'])
    last_name: str | None = Field(default=None, examples=['Пономорев'])