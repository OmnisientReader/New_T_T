from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import and_, or_
from typing import List, Optional
import datetime
from fastapi import HTTPException, status

from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation import ReservationCreate

async def get_reservation(db: AsyncSession, reservation_id: int) -> Optional[Reservation]:

    result = await db.execute(
        select(Reservation)
        .options(selectinload(Reservation.table))
        .filter(Reservation.id == reservation_id)
    )
    return result.scalar_one_or_none()

async def get_reservations(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Reservation]:

    result = await db.execute(
        select(Reservation)
        .options(selectinload(Reservation.table))
        .order_by(Reservation.reservation_time)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def delete_reservation(db: AsyncSession, reservation_id: int) -> Optional[Reservation]:

    db_reservation = await get_reservation(db, reservation_id)
    if db_reservation:
        await db.delete(db_reservation)
        await db.commit()
        return db_reservation
    return None

async def check_reservation_conflict(
    db: AsyncSession,
    table_id: int,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    exclude_reservation_id: Optional[int] = None
) -> bool:

    conflict_query = (
        select(Reservation)
        .filter(Reservation.table_id == table_id)
        .filter(

            Reservation.reservation_time < end_time,

             (Reservation.reservation_time + (Reservation.duration_minutes * datetime.timedelta(minutes=1))) > start_time

        )
    )


    if exclude_reservation_id is not None:
        conflict_query = conflict_query.filter(Reservation.id != exclude_reservation_id)


    result = await db.execute(conflict_query)
    conflicting_reservation = result.scalars().first()

    return conflicting_reservation is not None


async def create_reservation(db: AsyncSession, reservation: ReservationCreate) -> Reservation:


    table = await db.get(Table, reservation.table_id)
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with id {reservation.table_id} not found"
        )


    start_time = reservation.reservation_time
    end_time = start_time + datetime.timedelta(minutes=reservation.duration_minutes)


    has_conflict = await check_reservation_conflict(db, reservation.table_id, start_time, end_time)

    if has_conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Table {reservation.table_id} is already booked during the requested time slot ({start_time} to {end_time})."
        )


    db_reservation = Reservation(**reservation.model_dump())


    db.add(db_reservation)
    await db.commit()
    await db.refresh(db_reservation)


    await db.execute(
        select(Reservation).options(selectinload(Reservation.table)).filter(Reservation.id == db_reservation.id)
    )
    await db.refresh(db_reservation, attribute_names=['table'])


    return db_reservation
