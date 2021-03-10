from typing import List
from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from data.database import DbSession
from data.schema.users import User, UserBase, UserIn
from controllers.users import UserController

router = APIRouter()

fake_secret_token = "coneofsilence"


@router.post(
    "/api/users",
    summary="Return data of the created user",
    response_model=User,
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Token invalid or user already exists"},
    },
    status_code=201,
    tags=["Users"],
)
async def create(
    user: UserIn, x_token: str = Header(None), db_session: Session = Depends(DbSession)
):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    try:
        return UserController(db_session).create(user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")


@router.get(
    "/api/users",
    summary="Return data from all users",
    response_model=List[User],
    responses={
        200: {"description": "Data from users"},
        400: {"description": "Invalid token"},
    },
    status_code=200,
    tags=["Users"],
)
async def get_data_from_all_users(
    x_token: str = Header(None), db_session: Session = Depends(DbSession)
):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    return UserController(db_session).get_all()


@router.get(
    "/api/users/{user_id}",
    summary="Return data for a especific user",
    response_model=User,
    responses={
        200: {"description": "Data from user"},
        400: {"description": "Invalid token"},
        404: {"description": "User not found"},
    },
    status_code=200,
    tags=["Users"],
)
async def get_data_from(
    user_id: int, x_token: str = Header(None), db_session: Session = Depends(DbSession)
):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    user = UserController(db_session).get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put(
    "/api/users/{user_id}",
    summary="Update data of a especific user",
    response_model=User,
    responses={
        200: {"description": "User updated"},
        400: {"description": "Invalid token"},
        404: {"description": "User not found"},
    },
    status_code=200,
    tags=["Users"],
)
async def update_user_from(
    user_id: int,
    user: UserBase,
    x_token: str = Header(None),
    db_session: Session = Depends(DbSession),
):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    user = UserController(db_session).update(user_id, user)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete(
    "/api/users/{user_id}",
    summary="Delete a especific user",
    responses={
        200: {"description": "User deleted"},
    },
    status_code=200,
    tags=["Users"],
)
async def delete_user_from(
    user_id: int, x_token: str = Header(None), db_session: Session = Depends(DbSession)
):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    try:
        UserController(db_session).delete(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")

    return {"detail": "User deleted successfully"}
