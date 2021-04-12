import os
import secrets

from typing import Any, Dict, Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):

    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM = os.getenv("ALGORITHM")

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str],
                               values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl="token",
        scopes={
            "full": "All Permissions",
            "default": "Default Permission",
            "read": "Read Permission",
            "write": "Write Permission",
            "delete": "Delete Permission",
            "put": "Put Permission",
        },
    )

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


settings = Settings()
