from fastapi import FastAPI
import uvicorn
from config import server_settings
from utils import hash_password
from orm import create_user, is_user_exists, dev_create_tables, dev_delete_tables
from cloud_storage_project.models.models_pydantic import CreateUserPyd
from cloud_storage_project.models.models_exception import UserExistsException


app = FastAPI()


@app.on_event("startup")
async def create_example_tables():
    await dev_create_tables()


@app.on_event("shutdown")
async def delete_example_tables():
    await dev_delete_tables()


@app.post("/user_registration")
async def user_registration(user: CreateUserPyd):
        user.password = hash_password(user.password)
        if await is_user_exists(user.username):
            raise UserExistsException()
        else:
            await create_user(user)
            return {"message": "User registered"}


if __name__ == "__main__":
        uvicorn.run(app, host=server_settings.SERVER_HOST, port=server_settings.SERVER_PORT)
