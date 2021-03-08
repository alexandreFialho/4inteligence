from typing import List
from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from data.database import get_db
from data.schema.address import Address, AddressIn

from controllers.address import Address_Controller

router = APIRouter()

fake_secret_token = "coneofsilence"


@router.post("/api/address",
             summary="Return data of the created address",
             response_model=Address,
             responses={
                 201: {"description": "Address created successfully"},
                 400: {"description": "Token invalid or address already exists"}
             },
             status_code=201,
             tags=["Address"])
async def create(address: AddressIn,
                 db: Session = Depends(get_db),
                 x_token: str = Header(None)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    try:
        return Address_Controller(db).create(address)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Address already exists")


@router.get("/api/address",
            summary="Return data from all Address",
            response_model=List[Address],
            responses={
                200: {"description": "Data from Address"},
                400: {"description": "Invalid token"}
            },
            status_code=200,
            tags=["Address"])
async def get_data_from_all_users(db: Session = Depends(get_db),
                                  x_token: str = Header(None)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    return Address_Controller(db).get_all()


@router.get("/api/address/{address_id}",
            summary="Return data for a especific address",
            response_model=Address,
            responses={
                200: {"description": "Data from address"},
                400: {"description": "Invalid token"},
                404: {"description": "Address not found"}
            },
            status_code=200,
            tags=["Address"])
async def get_data_from(address_id: int,
                        db: Session = Depends(get_db),
                        x_token: str = Header(None)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    address = Address_Controller(db).get(address_id)

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return address


@router.put("/api/address/{address_id}",
            summary="Update data of a especific address",
            response_model=Address,
            responses={
                200: {"description": "Address updated"},
                400: {"description": "Invalid token"},
                404: {"description": "Address not found"}
            },
            status_code=200,
            tags=["Address"])
async def update_user_from(address_id: int,
                           address: AddressIn,
                           db: Session = Depends(get_db),
                           x_token: str = Header(None)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    address = Address_Controller(db).update(address_id, address)

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return address


@router.delete("/api/address/{address_id}",
               summary="Delete a especific address",
               responses={
                   200: {"description": "Address deleted"},
               },
               status_code=200,
               tags=["Address"])
async def delete_user_from(address_id: int,
                           db: Session = Depends(get_db),
                           x_token: str = Header(None)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")

    try:
        Address_Controller(db).delete(address_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Address not found")

    return {"detail": "Address deleted successfully"}
