from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
from config import server_settings
from utils import hash_password, generate_token, verify_token, verify_password
from orm import create_user, is_user_exists, dev_create_tables, dev_delete_tables, get_user_data
from cloud_storage_project.models.models_pydantic import CreateUserPyd
from cloud_storage_project.models.models_exception import UserExistsException, InvalidAuthDataException


app = FastAPI()


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

# TODO: add roles; functions for saving files (must be only after authentication); chanhge on_event to "lifespan"; err 422 custom handler


if __name__ == "__main__":
        uvicorn.run(app, host=server_settings.SERVER_HOST, port=server_settings.SERVER_PORT)
