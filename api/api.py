from typing import Annotated

import uvicorn
from fastapi import Depends
from fastapi import Form, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database.async_db import DataBase as Db
from database.async_db import db as db_ins

app = FastAPI()


class Office(BaseModel):
    latitude: float
    longitude: float


class Req(BaseModel):
    rko: str | None = None
    officeType: str | None = None
    salePointFormat: str | None = None
    suoAvailability: str | None = None
    hasRamp: str | None = None
    kep: bool | None = None
    myBranch: bool | None = None
    function: list[str] | None = None


@app.get("/recom_office",
        responses={
            200: {"model": Office, "description": "Successful Response"},
        })
async def add_post_post(latitude: float, longitude: float, db: Db = Depends(db_ins)) ->Office:
    point = await db.get_near_one(latitude, longitude)

    return Office(latitude=point[0],longitude=point[1])


@app.post("/recom_office",
        responses={
            200: {"model": Office, "description": "Successful Response"},
        })
async def add_post_post(latitude: float, longitude: float, req: Req, db: Db = Depends(db_ins)) ->Office:
    point = await db.get_near_one(latitude, longitude)

    return Office(latitude=point[0],longitude=point[1])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8031)