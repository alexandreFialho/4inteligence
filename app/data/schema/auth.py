from typing import Optional, List
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class AuthUserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False


class AuthUserIn(AuthUserBase):
    password: str


class AuthUser(AuthUserBase):
    id: int

    class Config:
        orm_mode = True
