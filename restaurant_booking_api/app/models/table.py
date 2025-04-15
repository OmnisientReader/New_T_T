from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=True)

    reservations = relationship("Reservation", back_populates="table", cascade="all, delete-orphan", lazy="selectin")

    def __repr__(self):
        return f"<Table(id={self.id}, name='{self.name}', seats={self.seats})>"
