from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
import datetime

from app.schemas.table import Table


class ReservationBase(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime.datetime
    duration_minutes: int

    @field_validator('duration_minutes')
    def duration_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Duration must be a positive number of minutes')
        return v

    @field_validator('reservation_time')
    def reservation_time_must_be_in_future(cls, v):

         return v



class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int
    table: Optional[Table] = None
    model_config = ConfigDict(from_attributes=True)
