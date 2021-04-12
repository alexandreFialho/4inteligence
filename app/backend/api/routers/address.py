from fastapi import Depends, Security, status
from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError


from api.deps import get_current_user
from core.controllers.address import AddressController
from data.models import AuthUser
from data.database import DbSession
from data.schema.address import Address, AddressIn, AddressPut

router = APIRouter()

fake_secret_token = "coneofsilence"


@router.post(
    "/api/address/{user_id}",
    summary="Create address",
    response_model=Address,
    responses={
        201: {"description": "Address created successfully"},
        401: {"description": "Could not validate credentials, Not enough permissions"},
        400: {"description": "Address already exists, Invalid postal code"},
        404: {"description": "User not found"},
    },
    status_code=201,
    tags=["Address"],
)
async def create(
    user_id: int,
    address: AddressIn,
    current_user: AuthUser = Security(get_current_user, scopes=["full", "default"]),
    db_session: Session = Depends(DbSession),
):

    try:
        return AddressController(db_session).create(user_id, address)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Address already exists"
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid postal code"
        )
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.get(
    "/api/address",
    summary="Get all Address",
    response_model=List[Address],
    responses={
        200: {"description": "Data from Address"},
        401: {"description": "Could not validate credentials, Not enough permissions"},
    },
    status_code=200,
    tags=["Address"],
)
async def get_all(
    current_user: AuthUser = Security(get_current_user, scopes=["full", "default"]),
    db_session: Session = Depends(DbSession),
):
    return AddressController(db_session).get_all()


@router.get(
    "/api/address/{address_id}",
    summary="Get address",
    response_model=Address,
    responses={
        200: {"description": "Data from address"},
        401: {"description": "Could not validate credentials, Not enough permissions"},
        404: {"description": "Address not found"},
    },
    status_code=200,
    tags=["Address"],
)
async def get_data_from(
    address_id: int,
    current_user: AuthUser = Security(get_current_user, scopes=["full", "default"]),
    db_session: Session = Depends(DbSession),
):
    address = AddressController(db_session).get(address_id)

    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )

    return address


@router.put(
    "/api/address/{address_id}",
    summary="Update address",
    response_model=Address,
    responses={
        200: {"description": "Address updated"},
        401: {"description": "Could not validate credentials, Not enough permissions"},
        404: {"description": "Address not found"},
    },
    status_code=200,
    tags=["Address"],
)
async def update_user_from(
    address_id: int,
    address: AddressPut,
    current_user: AuthUser = Security(get_current_user, scopes=["full", "default"]),
    db_session: Session = Depends(DbSession),
):

    address = AddressController(db_session).update(address_id, address)

    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )

    return address


@router.delete(
    "/api/address/{address_id}",
    summary="Delete address",
    responses={
        204: {"description": "Address deleted"},
        401: {"description": "Could not validate credentials, Not enough permissions"},
        404: {"description": "Address not found"},
    },
    status_code=204,
    tags=["Address"],
)
async def delete_address_from(
    address_id: int,
    current_user: AuthUser = Security(get_current_user, scopes=["full", "default"]),
    db_session: Session = Depends(DbSession),
):
    try:
        AddressController(db_session).delete(address_id)
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
