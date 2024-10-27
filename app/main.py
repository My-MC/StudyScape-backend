from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from settings import Settings
from surrealdb import Surreal
from timetable import (
    TimeTable,
    insert_timetable,
    parse_timetable_from_csv,
    select_timetable,
)

settings = Settings()
db_connection = Surreal(f"ws://{settings.db_address}/rpc")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    yield
    print("server is now stopping")


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def status():
    return {"status": "Working"}


@app.get("/timetable")
async def timetable(class_id: str):
    return await select_timetable(connection=db_connection, class_id=class_id)


@app.post("/timetable")
async def post_timetable(class_id: str, file: UploadFile):
    timetable = TimeTable(id=class_id, table=await parse_timetable_from_csv(file))

    await insert_timetable(connection=db_connection, timetable=timetable)

    return timetable
