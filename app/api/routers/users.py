from typing import List
from fastapi import APIRouter, Header, Security, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.deps import DbSession, get_current_user
from data.schema.users import User, UserBase, UserIn
from data.schema.auth import AuthUser
from controllers.users import UserController

router = APIRouter()


@router.post(
    "/api/users",
    summary="Create user",
    response_model=User,
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "User already exists"},
        401: {"description": "Could not validate credentials, Not enough permissions"},
    },
    status_code=201,
    tags=["Users"],
)
async def create(
    user: UserIn,
    current_user: AuthUser = Security(get_current_user, scopes=["full", "default"]),
    db_session: Session = Depends(DbSession),
):
    """# End-point for create new users

    Args:
        user (UserIn): Schema for input user

        Headers:
            Authorization : Bearer {token}

        token scopes accepted = ["full", "default"]

    Raises:

        HTTPException: [
            400: User already exists,
            401: Could not validate credentials,
            401: Not enough permissions
        ]

    Returns:
        [User]: created
    """
    try:
        return UserController(db_session).create(user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")


@router.get(
    "/api/users",
    summary="Get all users",
    response_model=List[User],
    responses={
        200: {"description": "List of users"},
        401: {"description": "Could not validate credentials, Not enough permissions"},
    },
    status_code=200,
    tags=["Users"],
)
async def get_data_from_all_users(
    current_user: AuthUser = Security(get_current_user, scopes=["full", "default"]),
    db_session: Session = Depends(DbSession),
):
    """# End-point for get all users
    Args:

        user (UserIn): Schema for input user

        Headers:
            Authorization : Bearer {token}

        token scopes accepted = ["full", "default"]

    Returns:
        List[User]: List of users registered.
    """
    return UserController(db_session).get_all()


@router.get(
    "/api/users/{user_id}",
    summary="Get user",
    response_model=User,
    responses={
        200: {"description": "Data from user"},
        401: {"description": "Could not validate credentials, Not enough permissions"},
        404: {"description": "User not found"},
    },
    status_code=200,
    tags=["Users"],
)
async def get_data_from(
    user_id: int,
    current_user: AuthUser = Security(get_current_user, scopes=["full", "default"]),
    db_session: Session = Depends(DbSession),
):
    """# End-point for get user specified

    Args:

        user_id (int): Identifier of the user

        Headers:
            Authorization : Bearer {token}

        token scopes accepted = ["full", "default"]

    Raises:

        HTTPException: [
            404: User not found,
            401: Could not validate credentials,
            401: Not enough permissions
        ]

    Returns:
        [User]: Datas from user
    """

    user = UserController(db_session).get(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put(
    "/api/users/{user_id}",
    summary="Update user",
    response_model=User,
    responses={
        200: {"description": "User updated"},
        401: {"description": "Could not validate credentials, Not enough permissions"},
        404: {"description": "User not found"},
    },
    status_code=200,
    tags=["Users"],
)
async def update_user_from(
    user_id: int,
    user: UserBase,
    current_user: AuthUser = Security(get_current_user, scopes=["full", "default"]),
    db_session: Session = Depends(DbSession),
):
    """# End-point for update user especified

    Args:

        user_id (int): Identifier of the user
        user (UserBase): Schema for update user

        Headers:
            Authorization : Bearer {token}

        token scopes accepted = ["full", "default"]

    Raises:

        HTTPException: [
            404: User not found,
            401: Could not validate credentials,
            401: Not enough permissions
        ]

    Returns:
        [User]: User updated
    """
    user = UserController(db_session).update(user_id, user)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete(
    "/api/users/{user_id}",
    summary="Delete user",
    responses={
        204: {"description": "User deleted"},
    },
    status_code=204,
    tags=["Users"],
)
async def delete_user_from(
    user_id: int,
    current_user: AuthUser = Security(get_current_user, scopes=["full", "default"]),
    db_session: Session = Depends(DbSession),
):
    """# End-point for delete user especified

    Args:
        user_id (int): Identifier of the user

        Headers:
            Authorization : Bearer {token}

        token scopes accepted = ["full", "default"]

    Raises:

        HTTPException: [
            404: User not found,
            401: Could not validate credentials,
            401: Not enough permissions
        ]
    """
    try:
        UserController(db_session).delete(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
