from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Interval
from sqlalchemy.orm import relationship
from app.models.base import Base
import datetime

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False, index=True)
    reservation_time = Column(DateTime, nullable=False, index=True)

    duration_minutes = Column(Integer, nullable=False)

    table = relationship("Table", back_populates="reservations", lazy="selectin")

    @property
    def end_time(self) -> datetime.datetime:

        return self.reservation_time + datetime.timedelta(minutes=self.duration_minutes)

    def __repr__(self):
        return f"<Reservation(id={self.id}, table_id={self.table_id}, time='{self.reservation_time}', duration={self.duration_minutes})>"
