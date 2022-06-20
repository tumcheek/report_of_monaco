from datetime import datetime
from report_package import read_data
from models import *


def fill_tables(start_info, end_info, abbreviations):
    for start, end, abbreviation in zip(start_info, end_info, abbreviations):
        format_time = "%H:%M:%S.%f"
        delta_time = str(abs(datetime.strptime(end[1], format_time) - datetime.strptime(start[1], format_time)))[2:-3]
        driver = Driver.create(abbreviation=abbreviation[0], full_name=abbreviation[1], car=abbreviation[2])
        Time.create(driver_id=driver, date=start[0][3:], start_time=start[1], end_time=end[1], delta_time=delta_time)


if __name__ == '__main__':
    with db:
        db.create_tables([Driver, Time])
        fill_tables(read_data(DATA, 'start.log'), read_data(DATA, 'end.log'), read_data(DATA, 'abbreviations.txt'))





