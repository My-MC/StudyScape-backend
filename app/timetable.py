import csv
from io import StringIO

from fastapi import UploadFile
from pydantic import BaseModel
from settings import Settings
from surrealdb import Surreal

settings = Settings()


class TimeTable(BaseModel):
    id: str
    table: list[list[str]]


async def parse_timetable_from_csv(csv_file: UploadFile):
    contents = await csv_file.read()
    string_io = StringIO(contents.decode("utf-8"))

    csv_reader = csv.reader(string_io)
    data = [row for row in csv_reader][1:]
    return data


async def select_timetable(connection: Surreal, class_id: str):
    async with connection as db:
        await db.signin({"user": settings.db_user, "pass": settings.db_password})
        await db.use(settings.db_namespace, settings.db_database)
        result = await db.query(
            "SELECT * FROM timetable WHERE id = $class_id LIMIT 1",
            {"class_id": f"timetable:{class_id}"},
        )

    return result[0]["result"][0]


async def insert_timetable(connection: Surreal, timetable: TimeTable):
    async with connection as db:
        await db.signin({"user": settings.db_user, "pass": settings.db_password})
        await db.use(settings.db_namespace, settings.db_database)
        await db.create("timetable", timetable.model_dump())
