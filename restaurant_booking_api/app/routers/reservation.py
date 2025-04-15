from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.reservation import Reservation, ReservationCreate
from app.services import reservation as reservation_service

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"],
    responses={
        404: {"description": "Not found"},
        409: {"description": "Conflict"}
    },
)

@router.post("/", response_model=Reservation, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation: ReservationCreate,
    db: AsyncSession = Depends(get_db)
):

    try:
        return await reservation_service.create_reservation(db=db, reservation=reservation)
    except HTTPException as e:

        raise e
    except Exception as e:

        print(f"Error creating reservation: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/", response_model=List[Reservation])
async def read_reservations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):

    reservations = await reservation_service.get_reservations(db, skip=skip, limit=limit)
    return reservations

@router.get("/{reservation_id}", response_model=Reservation)
async def read_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db)
):

    db_reservation = await reservation_service.get_reservation(db, reservation_id=reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@router.delete("/{reservation_id}", response_model=Reservation)
async def delete_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db)
):

    deleted_reservation = await reservation_service.delete_reservation(db, reservation_id=reservation_id)
    if deleted_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return deleted_reservation
