from pydantic import BaseModel


class RegisterInfo(BaseModel):
    email: str
    password: str
    password_check: str


class LoginInfo(BaseModel):
    email: str
    password: str
