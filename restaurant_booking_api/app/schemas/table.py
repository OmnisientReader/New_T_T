from pydantic import BaseModel, ConfigDict
from typing import Optional


class TableBase(BaseModel):
    name: str
    seats: int
    location: Optional[str] = None


class TableCreate(TableBase):
    pass


class Table(TableBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
