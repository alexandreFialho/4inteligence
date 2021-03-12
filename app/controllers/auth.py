from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from sqlalchemy.orm import Session

from api import config
from data.models import AuthUser
from data.schema.auth import AuthUserIn
from controllers.base_controller import CONTROLLER


def verify_password(plain_password, hashed_password):
    return config.pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return config.pwd_context.hash(password)


def get_user(db_session: Session, username: str) -> AuthUser:
    return db_session.query(AuthUser).filter_by(username=username).first()


def authenticate_user(db_session: Session, username: str, password: str):
    user = get_user(db_session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        config.SECRET_KEY,
        algorithm=config.ALGORITHM
    )
    return encoded_jwt


class AuthUserController(CONTROLLER):
    def __init__(self, db_session: Session):
        super(AuthUserController, self).__init__(
            db_session=db_session, db_entity=AuthUser
        )

    def create(self, auth_user: AuthUserIn):
        auth_user.password = get_password_hash(
            auth_user.password)
        auth_user_db = AuthUser(**auth_user.dict())
        self.db_session.add(auth_user_db)
        self.db_session.commit()
        return self.get(auth_user_db.id)
