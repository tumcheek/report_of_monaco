from peewee import *
from report_package import read_data, print_report, build_report
from pathlib import Path
from datetime import datetime


ROOT = Path().resolve().parent
DATA = ROOT / 'Data'

db = SqliteDatabase(DATA / 'report.db')


class Driver(Model):
    abbreviation = CharField()
    full_name = CharField()
    car = CharField()
    date = DateField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    delta_time = DateTimeField()

    class Meta:
        database = db


def create_table_drivers(start_info, end_info, abbreviations):
    for start, end, abbreviation in zip(start_info, end_info, abbreviations):
        format_time = "%H:%M:%S.%f"
        delta_time = str(abs(datetime.strptime(end[1], format_time) - datetime.strptime(start[1], format_time)))[2:-3]
        Driver.create(abbreviation=abbreviation[0], full_name=abbreviation[1], car=abbreviation[2], date=start[0][3:],
                      start_time=start[1], end_time=end[1], delta_time=delta_time)


if __name__ == '__main__':
    with db:
        db.create_tables([Driver])
        create_table_drivers(read_data(DATA, 'start.log'), read_data(DATA, 'end.log'), read_data(DATA, 'abbreviations.txt'))




