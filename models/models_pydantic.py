from pydantic import BaseModel, constr


class CreateUserPyd(BaseModel):
    username: str
    password: str
    memory_usage: int | None = None
    memory_limit: int | None = None

