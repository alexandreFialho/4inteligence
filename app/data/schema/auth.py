from typing import Optional, List
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiYWxndW1hIGluZm9ybWFjYW8iLCJzY29wZXMiOiJhbGd1bnMgZXNjb3BvcyIsImV4cCI6MTYxNTU4NDczN30.l4uvnF8mKJWJbmsrgqIaQAHwmMmVFLGvWMIHjxtgZYs"
    token_type: str = "Bearer"


class TokenData(BaseModel):
    username: Optional[str]
    scopes: List[str] = []


class AuthUserBase(BaseModel):
    username: str
    email: Optional[str] = "email@email.com"


class AuthUserIn(AuthUserBase):
    password: str


class AuthUser(AuthUserBase):
    id: int

    class Config:
        orm_mode = True
