from peewee import *
from pathlib import Path


ROOT = Path().resolve().parent
DATA = ROOT / 'Data'
REPORT_DB = 'report.db'

db = SqliteDatabase(DATA / REPORT_DB)


class BaseModel(Model):
    class Meta:
        database = db


class Driver(BaseModel):
    abbreviation = CharField()
    full_name = CharField()
    car = CharField()

    class Meta:
        db_table = 'drivers'


class Time(BaseModel):
    driver_id = ForeignKeyField(Driver, on_delete='CASCADE')
    date = DateField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    delta_time = DateTimeField()
