from fastapi import HTTPException


class UserExistsException(HTTPException):
    def __init__(self, status_code=409, detail="User already exists"):
        self.status_code = status_code
        self.detail = detail
        self.headers = {"WWW-Authenticate": "Bearer"}


class TokenExpiredException(HTTPException):
    def __init__(self, status_code=401, detail="Token has expired"):
        self.status_code = status_code
        self.detail = detail
        self.headers = {"WWW-Authenticate": "Bearer"}


class TokenDecodeException(HTTPException):
    def __init__(self, status_code=401, detail="Invalid token"):
        self.status_code = status_code
        self.detail = detail
        self.headers = {"WWW-Authenticate": "Bearer"}


class InvalidAuthDataException(HTTPException):
    def __init__(self, status_code=401, detail="Invalid username or password"):
        self.status_code = status_code
        self.detail = detail
        self.headers = {"WWW-Authenticate": "Bearer"}

