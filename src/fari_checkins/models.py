from typing import List, Optional
from sqlalchemy import func, ForeignKey
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Resident(Base):
    __tablename__ = "resident"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    address: Mapped[str]
    number: Mapped[str]
    checkins: Mapped[List["Checkin"]] = relationship(back_populates="resident")
    caregivers: Mapped[List["Caregiver"]] = relationship(back_populates="resident")


class Caregiver(Base):
    __tablename__ = "caregiver"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    number: Mapped[str]
    res_id: Mapped[int] = mapped_column(ForeignKey("resident.id"))
    resident: Mapped["Resident"] = relationship(back_populates="caregivers")


class Checkin(Base):
    __tablename__ = "checkin"
    id: Mapped[int] = mapped_column(primary_key=True)
    res_id: Mapped[int] = mapped_column(ForeignKey("resident.id"))
    timestamp: Mapped[datetime] = mapped_column(default=func.now())
    mood: Mapped[str]
    category: Mapped[str]
    notes: Mapped[Optional[str]]
    resident: Mapped["Resident"] = relationship(back_populates="checkins")
