from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
import datetime
from config import JWT_ALGORITHM, TOKEN_EXP_TIME, SECRET_KEY
from cloud_storage_project.models.models_exception import TokenExpiredException, TokenDecodeException



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