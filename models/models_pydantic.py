from pydantic import BaseModel, constr


class CreateUserPyd(BaseModel):
    username: str
    password: str

