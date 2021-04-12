from fastapi import HTTPException, status, Depends
from fastapi.security import SecurityScopes
from sqlalchemy.orm import Session
from pydantic import ValidationError
from jose import JWTError, jwt

from core.config import settings
from core.controllers.auth import get_user
from data.database import DbSession
from data.schema.auth import TokenData


async def get_current_user(security_scopes: SecurityScopes,
                           token: str = Depends(settings.oauth2_scheme),
                           db_session: Session = Depends(DbSession)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", ["default"])
        if not token_scopes:
            token_scopes = ["default"]
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = get_user(db_session, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in token_data.scopes:
        if scope in security_scopes.scopes:
            return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not enough permissions",
        headers={"WWW-Authenticate": authenticate_value},
    )
