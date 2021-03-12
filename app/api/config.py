import os

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SERVER_TEST = os.getenv("POSTGRES_SERVER_TEST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "full": "All Permissions",
        "default": "Default Permission",
        "read": "Read Permission",
        "write": "Write Permission",
        "delete": "Delete Permission",
        "put": "Put Permission"
    },
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
