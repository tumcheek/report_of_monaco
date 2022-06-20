from peewee import *
from pathlib import Path


ROOT = Path().resolve().parent
DATA = ROOT / 'Data'
REPORT_DB = 'report.database'

db = SqliteDatabase(DATA / REPORT_DB)


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


class Driver(BaseModel):
    abbreviation = CharField()
    full_name = CharField()
    car = CharField()

    class Meta:
        db_table = 'drivers'


class Time(BaseModel):
    driver_id = ForeignKeyField(Driver)
    date = DateField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    delta_time = DateTimeField()
