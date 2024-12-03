import traceback

import psutil
from fastapi import Depends, UploadFile
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
import datetime
from config import JWT_ALGORITHM, TOKEN_EXP_TIME, SECRET_KEY, INITIAL_DIR
from cloud_storage_project.models.models_exception import TokenExpiredException, TokenDecodeException,\
                                                          UserFileNotFoundException, NotEnoughUserMemoryException,\
                                                          NotEnoughServerMemoryException
import aiofiles
import os
from orm import get_user_data
import psutil
from orm import update_user_data


pwd_context = CryptContext(schemes=['bcrypt'])

security_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def generate_token(username: str) -> str:
    payload = {"username": username, "exp": datetime.datetime.now() + TOKEN_EXP_TIME}
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def verify_token(token: str = Depends(security_scheme)) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException()
    except jwt.DecodeError:
        raise TokenDecodeException()


async def is_enough_user_memory(username: str, file_size: int):
    user = await get_user_data(username)
    if (user.memory_usage + file_size) >= user.memory_limit:
        return False
    return True


def is_enough_server_memory(file_size: int):
    disk_info = psutil.disk_usage("/")
    print(disk_info)
    if disk_info.free <= file_size:
        return False
    return True

async def update_user_memory_usage(username: str, file_size: int):
    user = await get_user_data(username)
    user.memory_usage = user.memory_usage + file_size
    await update_user_data(user)


async def save_user_file(user_file: UploadFile, path: str, username: str, buffer_size=1024*1024*0.5) -> bool:
    if not user_file:
        raise UserFileNotFoundException()
    if not await is_enough_user_memory(username, user_file.size):
        raise NotEnoughUserMemoryException()
    if not is_enough_server_memory(user_file.size):
        raise NotEnoughServerMemoryException()

    buffer_size = int(buffer_size)
    path = os.path.join(INITIAL_DIR, username, path, user_file.filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    async with aiofiles.open(path, "wb") as local_file:
        try:

            while True:
                chunk = await user_file.read(buffer_size)
                if not chunk:
                    break
                await local_file.write(chunk)

        except Exception as e:
            print("FILE SAVE ERROR")
            print(traceback.format_exc(e))
            print("____________")
            # delete corrupted file
            if os.path.exists(path):
                os.remove(path)
            # close user file transmission
            await user_file.close()
            return False

    await update_user_memory_usage(username, user_file.size)
    await user_file.close()
    return True