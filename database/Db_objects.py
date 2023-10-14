from __future__ import annotations
import datetime
from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import Any, List


class Base(DeclarativeBase):
    pass


class Branch(Base):
    __tablename__ = 'branches'
    id: Mapped[int] = mapped_column(primary_key=True)
    salepointname: Mapped[str]
    address: Mapped[str]
    rko: Mapped[str]
    officetype: Mapped[str]
    salepointformat: Mapped[str]
    suoavailability: Mapped[str]
    hasramp: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    metrostation: Mapped[str]
    distance: Mapped[float]
    kep: Mapped[bool]
    mybranch: Mapped[bool]
    functions: Mapped[List["Function"]] = relationship(back_populates="branch")


class Function(Base):
    __tablename__ = 'functions'
    id: Mapped[int] = mapped_column(primary_key=True)
    function_name: Mapped[str]
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))
    branch: Mapped["Branch"] = relationship(back_populates="functions")