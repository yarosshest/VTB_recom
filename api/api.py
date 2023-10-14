from typing import Annotated

from fastapi import Depends
from fastapi import Form, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database.async_db import DataBase as Db
from database.async_db import db as db_ins


app = FastAPI()


@app.post("/recom",
             responses={
                 200: {"model": Message, "description": "Successful Response"},
             })
async def add_post_post(autor: Annotated[str, Form()],
                        topic: Annotated[str, Form()],
                        body: Annotated[str, Form()],
                        db: Db = Depends(db_ins)
                        ):
    await db.add_post(autor, topic, body)
    return JSONResponse(status_code=200, content={"message": "Successful Response"})
