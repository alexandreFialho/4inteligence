from typing import List
from fastapi import APIRouter, Header

from data.schema.users import User, UserBase

router = APIRouter()

fake_secret_token = "coneofsilence"


@router.post("/api/users",
             summary="Return data of the created user",
             response_model=User,
             responses={
                 201: {"description": "User created successfully"},
             },
             status_code=201,
             tags=["Users"])
async def create(user: UserBase, x_token: str = Header(None)):
    return {"message": "User created successfully"}


@router.get("/api/users",
            summary="Return data from all users",
            response_model=List[User],
            responses={
                200: {"description": "Data from users"},
            },
            status_code=200,
            tags=["Users"])
async def get_data_from_all_users(x_token: str = Header(None)):
    return {"message": "data from all users"}


@router.get("/api/users/{user_id}",
            summary="Return data for a especific user",
            response_model=User,
            responses={
                200: {"description": "Data from user"},
            },
            status_code=200,
            tags=["Users"])
async def get_data_from(user_id: int, x_token: str = Header(None)):
    return {"message": f"data from user: {user_id}"}


@router.put("/api/users/{user_id}",
            summary="Update data of a especific user",
            response_model=User,
            responses={
                200: {"description": "User updated"},
            },
            status_code=204,
            tags=["Users"])
async def update_user_from(user_id: int, x_token: str = Header(None)):
    return {"message": f"User Updated: {user_id}"}


@router.delete("/api/users/{user_id}",
               summary="Delete a especific user",
               responses={
                   204: {"description": "User deleted"},
               },
               status_code=204,
               tags=["Users"])
async def delete_user_from(user_id: int, x_token: str = Header(None)):
    return {"message": f"User Deleted: {user_id}"}
