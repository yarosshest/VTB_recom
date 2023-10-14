from __future__ import annotations

import asyncio
import configparser
import pathlib
import tracemalloc
from typing import List

from sqlalchemy import NullPool, MetaData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import selectinload, joinedload, contains_eager
from haversine import haversine, Unit

from database.Db_objects import Branch, Function, Base

meta = MetaData()

p = pathlib.Path(__file__).parent.parent.joinpath('config.ini')

config = configparser.ConfigParser()
config.read(p)

BDCONNECTION = config['DEFAULT']["BDCONNECTION"]


class DataBase:
    def __init__(self):
        print("db class inited")

    def __call__(self):
        return self

    engine = create_async_engine(
        BDCONNECTION,
        echo=False,
        poolclass=NullPool,
    )

    async def get_session(self) -> AsyncSession:
        async with async_sessionmaker(self.engine, expire_on_commit=True)() as async_session:
            await async_session.begin()
            return async_session

    async def get_brances(self) -> List[Branch]:
        session = await self.get_session()
        q = select(Branch).join(Function, Function.branch_id == Branch.id).options(contains_eager(Branch.functions))
        posts = (await session.execute(q)).scalars().unique().fetchall()
        res = []
        for i in posts:
            res.append(i)
        session.expunge_all()
        return res

    async def get_near_one(self, lat: float, lon: float) -> list[float]:
        session = await self.get_session()
        q = select(Branch).join(Function, Function.branch_id == Branch.id).options(contains_eager(Branch.functions))
        posts = (await session.execute(q)).scalars().unique().fetchall()
        res = []

        for i in posts:
            h = haversine((i.latitude, i.longitude), (lat, lon))
            lot_lon = [h, i.latitude, i.longitude]

            res.append(lot_lon)
        res.sort(key=lambda x: x[0])
        return res[0][1:]


db = DataBase()

if __name__ == "__main__":
    tracemalloc.start()
