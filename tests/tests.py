from rest_api_report import app, create_report_dict, create_drivers_dict
from flask import request
from pathlib import Path

ROOT = Path().resolve().parent
DATA_DIR = ROOT / 'Data'

client = app.test_client()


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


def test_create_report_dict():
    report = '1. Daniel Ricciardo | RED BULL RACING TAG HEUER | 1:12.013'
    convert_result = {'1': {'number':'1', 'name': 'Daniel Ricciardo', 'car': 'RED BULL RACING TAG HEUER', 'time': '1:12.013'}}
    assert create_report_dict(report) == convert_result


def test_convert_drivers_to_json():
    driver = [('BHS', 'Brendon Hartley', 'SCUDERIA TORO ROSSO HONDA')]
    result = {'BHS': {'abbreviation': 'BHS', 'car': 'SCUDERIA TORO ROSSO HONDA', 'name': 'Brendon Hartley'}}
    assert create_drivers_dict(driver) == result


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
