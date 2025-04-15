from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.table import Table, TableCreate
from app.services import table as table_service

router = APIRouter(
    prefix="/tables",
    tags=["Tables"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Table, status_code=status.HTTP_201_CREATED)
async def create_table(
    table: TableCreate,
    db: AsyncSession = Depends(get_db)
):

    return await table_service.create_table(db=db, table=table)

@router.get("/", response_model=List[Table])
async def read_tables(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):

    tables = await table_service.get_tables(db, skip=skip, limit=limit)
    return tables

@router.get("/{table_id}", response_model=Table)
async def read_table(
    table_id: int,
    db: AsyncSession = Depends(get_db)
):

    db_table = await table_service.get_table(db, table_id=table_id)
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return db_table

@router.delete("/{table_id}", response_model=Table)
async def delete_table(
    table_id: int,
    db: AsyncSession = Depends(get_db)
):

    deleted_table = await table_service.delete_table(db, table_id=table_id)
    if deleted_table is None:
        raise HTTPException(status_code=404, detail="Table not found")

    return deleted_table
