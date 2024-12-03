from fastapi import FastAPI, Depends, UploadFile, Body
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
from config import server_settings, INITIAL_DIR
from utils import hash_password, generate_token, verify_token, verify_password, save_user_file
from orm import create_user, is_user_exists, dev_create_tables, dev_delete_tables, get_user_data
from cloud_storage_project.models.models_pydantic import CreateUserPyd
from cloud_storage_project.models.models_exception import UserExistsException, InvalidAuthDataException
import os


app = FastAPI()
os.makedirs(INITIAL_DIR, exist_ok=True)


# DEV: func for dev only
@app.on_event("startup")
async def create_example_tables():
    await dev_create_tables()


# DEV: func for dev only
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
            token = generate_token(user.username)
            return {"message": "User registered",
                    "token": token}


@app.get("/login")
async def user_authentication(form_data=Depends(OAuth2PasswordRequestForm)):
    user = await get_user_data(form_data.username)
    if user and verify_password(form_data.password, user.password):
        token = generate_token(user.username)
        return {"message": "User authenticated",
                "token": token}
    else:
        raise InvalidAuthDataException()


@app.post("/load_file")
async def load_file(user_file: UploadFile, path: str = Body(...), payload=Depends(verify_token)):
    await save_user_file(user_file, path, payload["username"])
    return {"message": "user file have been saved"}


@app.get("/get/{username}")
async def get_user_info(username):
    user = await get_user_data(username)
    if user:
        return {"username": user.username,
                "mem_usage": user.memory_usage,
                "mem_limit": user.memory_limit,
                "percent_mem_usage": user.memory_usage / user.memory_limit}
    else:
        return {"massage": "user not found"}


# TODO: add roles; /get/{username} - only admin access; change on_event to "lifespan"; err 422 custom handler


if __name__ == "__main__":
    uvicorn.run(app, host=server_settings.SERVER_HOST, port=server_settings.SERVER_PORT)
