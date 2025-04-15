from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models.table import Table
from app.schemas.table import TableCreate

async def get_table(db: AsyncSession, table_id: int) -> Optional[Table]:

    result = await db.execute(select(Table).filter(Table.id == table_id))
    return result.scalar_one_or_none()

async def get_tables(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Table]:

    result = await db.execute(
        select(Table)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_table(db: AsyncSession, table: TableCreate) -> Table:

    db_table = Table(**table.model_dump())
    db.add(db_table)
    await db.commit()
    await db.refresh(db_table)
    return db_table

async def delete_table(db: AsyncSession, table_id: int) -> Optional[Table]:

    db_table = await get_table(db, table_id)
    if db_table:
        await db.delete(db_table)
        await db.commit()
        return db_table
    return None
