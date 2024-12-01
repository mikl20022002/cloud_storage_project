from fastapi import HTTPException


class UserExistsException(HTTPException):
    def __init__(self, status_code=409, detail="User already exists"):
        self.status_code = status_code
        self.detail = detail
