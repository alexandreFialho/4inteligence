from fastapi import Depends
from typing import List
from fastapi import APIRouter, Header, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, InvalidRequestError


from data.database import DbSession
from data.schema.address import Address, AddressIn
from controllers.address import AddressController

router = APIRouter()

fake_secret_token = "coneofsilence"


@router.post(
    "/api/address",
    summary="Return data of the created address",
    response_model=Address,
    responses={
        201: {"description": "Address created successfully"},
        400: {"description": "Token invalid or address already exists"},
    },
    status_code=201,
    tags=["Address"],
)
async def create(
    address: AddressIn,
    x_token: str = Header(None),
    db_session: Session = Depends(DbSession)
):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    
    print(36, dict(address.dict()))
    try:
        return AddressController(db_session).create(address)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Address already exists")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid postal code")


@router.get(
    "/api/address",
    summary="Return data from all Address",
    response_model=List[Address],
    responses={
        200: {"description": "Data from Address"},
        400: {"description": "Invalid token"},
    },
    status_code=200,
    tags=["Address"],
)
async def get_all(
    x_token: str = Header(None),
    db_session: Session = Depends(DbSession)
):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    return AddressController(db_session).get_all()


@router.get(
    "/api/address/{address_id}",
    summary="Return data for a especific address",
    response_model=Address,
    responses={
        200: {"description": "Data from address"},
        400: {"description": "Invalid token"},
        404: {"description": "Address not found"},
    },
    status_code=200,
    tags=["Address"],
)
async def get_data_from(
    address_id: int,
    x_token: str = Header(None),
    db_session: Session = Depends(DbSession)
):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    address = AddressController(db_session).get(address_id)

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return address


@router.put(
    "/api/address/{address_id}",
    summary="Update data of a especific address",
    response_model=Address,
    responses={
        200: {"description": "Address updated"},
        400: {"description": "Invalid token"},
        404: {"description": "Address not found"},
    },
    status_code=200,
    tags=["Address"],
)
async def update_user_from(
    address_id: int,
    address: AddressIn,
    x_token: str = Header(None),
    db_session: Session = Depends(DbSession)
):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    address = AddressController(db_session).update(address_id, address)

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return address


@router.delete(
    "/api/address/{address_id}",
    summary="Delete a especific address",
    responses={
        204: {"description": "Address deleted"},
    },
    status_code=204,
    tags=["Address"],
)
async def delete_address_from(
    address_id: int,
    x_token: str = Header(None),
    db_session: Session = Depends(DbSession)
):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    try:
        AddressController(db_session).delete(address_id)
        return
    except InvalidRequestError:
        raise HTTPException(status_code=404, detail="Address not found")
