from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.config import ACCESS_TOKEN_EXPIRE_MINUTES
from api.deps import DbSession
from data.schema.auth import AuthUser, AuthUserIn, Token
from controllers.auth import create_access_token, authenticate_user, AuthUserController


router = APIRouter()


@router.post(
    "/api/auth",
    summary="Create login",
    response_model=AuthUser,
    responses={
        201: {"description": "Auth user created successfully"},
        400: {"description": "Auth already exists"},
    },
    status_code=201,
    tags=["Security"],
)
async def create_login(auth_user: AuthUserIn, db_session: Session = Depends(DbSession)):
    try:
        user = AuthUserController(db_session=db_session).create(auth_user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Auth already exists"
        )

    return user


@router.post(
    "/token",
    summary="Create token",
    response_model=Token,
    responses={
        201: {"description": "Access token created"},
        401: {"description": "Incorrect username or password"},
    },
    status_code=201,
    tags=["Security"],
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(DbSession),
):
    user = authenticate_user(
        db_session=db_session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
