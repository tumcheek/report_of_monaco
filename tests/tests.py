from rest_api_report import app, create_report_dict, create_drivers_dict
from flask import request
from pathlib import Path
from peewee import *
from pytest import fixture

ROOT = Path().resolve().parent
DATA_DIR = ROOT / 'Data'

client = app.test_client()
db = SqliteDatabase(DATA_DIR / 'test.db')


@fixture()
def bd_query():
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

    return Driver.select().order_by(Driver.delta_time)


def test_create_report_dict(bd_query):
    result = {'1': {'car': 'SAUBER FERRARI',
                    'name': 'Charles Leclerc',
                    'number': '1',
                    'time': '01:12.829'},
              '2': {'car': 'RENAULT',
                    'name': 'Carlos Sainz',
                    'number': '2',
                    'time': '01:12.950'},
              '3': {'car': 'SCUDERIA TORO ROSSO HONDA',
                    'name': 'Brendon Hartley',
                    'number': '3',
                    'time': '01:13.179'}}

    assert create_report_dict(bd_query) == result


def test_create_driver_dict(bd_query):
    result = {'BHS': {'abbreviation': 'BHS',
                      'car': 'SCUDERIA TORO ROSSO HONDA',
                      'name': 'Brendon Hartley'},
              'CLS': {'abbreviation': 'CLS',
                      'car': 'SAUBER FERRARI',
                      'name': 'Charles Leclerc'},
              'CSR': {'abbreviation': 'CSR', 'car': 'RENAULT', 'name': 'Carlos Sainz'}}
    assert create_drivers_dict(bd_query) == result


def test_non_existent_index():
    response = client.get('/')
    assert response.status_code == 404


def test_report():
    response = client.get('/report')
    assert response.status_code == 200


def test_drivers():
    response = client.get('/report/drivers/')
    assert response.status_code == 200


def test_request_order():
    with client as c:
        response = c.get('/report?order=desc')
        assert request.args['order'] == 'desc'


def test_driver_statistic():
    with client as c:
        response = c.get('/report/drivers/?driver_id=AAA')
        assert request.args['driver_id'] == 'AAA'


def test_report_api():
    with client as c:
        response = c.get('/api/v1/report/?format=xml')
        assert request.args['format'] == 'xml'


def test_driver_api():
    with client as c:
        response = c.get('/api/v1/report/drivers?format=xml&driver_id=SVF')
        assert request.args['format'] == 'xml'
        assert request.args['driver_id'] == 'SVF'


def test_drivers_api():
    with client as c:
        response = c.get('/api/v1/report/drivers?format=xml')
        assert request.args['format'] == 'xml'
