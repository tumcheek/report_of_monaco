from datetime import datetime
from report_package import read_data
from models import *
import argparse

START_LOG = 'start.log'
END_LOG = 'end.log'
ABBREVIATION = 'abbreviations.txt'


def fill_tables(start_info, end_info, abbreviations):
    for start, end, abbreviation in zip(start_info, end_info, abbreviations):
        format_time = "%H:%M:%S.%f"
        delta_time = str(abs(datetime.strptime(end[1], format_time) - datetime.strptime(start[1], format_time)))[2:-3]
        driver = Driver.create(abbreviation=abbreviation[0], full_name=abbreviation[1], car=abbreviation[2])
        Time.create(driver_id=driver, date=start[0][3:], start_time=start[1], end_time=end[1], delta_time=delta_time)


def cli_fill_tables():
    parser = argparse.ArgumentParser(description='Fills database table')
    parser.add_argument('--folder_path', default=DATA, type=str)
    parser.add_argument('--start_log', default=START_LOG, type=str)
    parser.add_argument('--end_log', default=END_LOG, type=str)
    parser.add_argument('--abr_txt', default=ABBREVIATION, type=str)
    args = parser.parse_args()
    return fill_tables(read_data(args.folder_path, args.start_log), read_data(args.folder_path, args.end_log),
                       read_data(args.folder_path, args.abr_txt))


if __name__ == '__main__':
    with db:
        db.create_tables([Driver, Time])
        cli_fill_tables()
