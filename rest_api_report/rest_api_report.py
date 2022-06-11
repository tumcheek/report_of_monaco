from flask import Flask, request, render_template, Response
from flask_restful import Resource, Api
import report_package.report
from report_package import *
from pathlib import Path
from flasgger import Swagger
from dicttoxml import dicttoxml
import json

ROOT = Path().resolve().parent
DATA_DIR = ROOT / 'Data'

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)


def create_report_dict(report):
    report_list = list(map(lambda item: item.split('|'), report.split('\n')))
    report_dict = {}
    for item in report_list:
        if '' in item:
            continue
        if '-' in item[0]:
            continue
        name = item[0].split('. ')[1]
        number = item[0].split('. ')[0]
        report_dict[number] = {'number': number,
                               'name': name.strip(),
                               'car': item[1].strip(),
                               'time': item[2].strip()}
    return report_dict


def create_drivers_dict(data):
    data_dict = {}
    for driver_info in data:
        data_dict[driver_info[0]] = {
                'abbreviation': driver_info[0],
                'name': driver_info[1],
                'car': driver_info[2]
            }
    return data_dict


def make_driver_statistic(driver_abr, drivers_report):
    report = print_report(build_report(DATA_DIR), DATA_DIR).split('\n')
    for driver_info in drivers_report:
        if driver_abr in driver_info:
            for statistic_driver in report:
                if driver_info[1] in statistic_driver:
                    return statistic_driver


@app.route('/report')
def show_report():
    order = request.args.get('order')
    report = reversed(print_report(build_report(DATA_DIR), DATA_DIR).split('\n')) if order == 'desc' \
        else print_report(build_report(DATA_DIR), DATA_DIR).split('\n')
    return render_template('index.html', report=report)


@app.route('/report/drivers/')
def show_drivers():
    driver_abr = request.args.get('driver_id')
    order = request.args.get('order')
    drivers_list = reversed(read_data(DATA_DIR, report_package.report.ABBREVIATIONS)) if order == 'desc' \
        else read_data(DATA_DIR, report_package.report.ABBREVIATIONS)
    if driver_abr:
        return make_driver_statistic(driver_abr, drivers_list)
    return render_template('drivers.html', drivers_report=drivers_list)


class Report(Resource):
    def get(self):
        """
        ---
        parameters:
          - name: format
            in: query
            type: string
            enum: ['json', 'xml']
            required: true
        responses:
          200:
            description: The report of monaco
            schema:
              id: report
              properties:
                format:
                  type: string
                  description: The format of  data
                  default: json
        """
        format = request.args.get('format')
        report_dict = create_report_dict(print_report(build_report(DATA_DIR), DATA_DIR))
        if format == 'json':
            return Response(json.dumps(report_dict), mimetype='application/json')
        elif format == 'xml':
            return Response(dicttoxml(report_dict), mimetype='text/xml')


class Drivers(Resource):
    def get(self):
        """
        ---
        parameters:
          - name: format
            in: query
            type: string
            enum: ['json', 'xml']
            required: true
          - name: driver_id
            in: query
            type: string
            required: false
        responses:
          200:
            description: The drivers statistic
            schema:
              id: drivers
              properties:
                format:
                  type: string
                  description: The format of  data
                  default: json
                driver_id:
                  type: string
                  description: The abbreviation of  driver
                  default: None
        """
        driver_abr = request.args.get('driver_id')
        format = request.args.get('format')
        drivers_dict = create_drivers_dict(read_data(DATA_DIR, report_package.report.ABBREVIATIONS))
        if driver_abr:
            driver_data = make_driver_statistic(driver_abr, read_data(DATA_DIR, report_package.report.ABBREVIATIONS))
            report_dict = create_report_dict(driver_data)
            if format == 'json':
                return Response(json.dumps(report_dict), mimetype='application/json')
            elif format == 'xml':
                return Response(dicttoxml(report_dict), mimetype='text/xml')
        if format == 'json':
            return Response(json.dumps(drivers_dict), mimetype='application/json')
        elif format == 'xml':
            return Response(dicttoxml(drivers_dict), mimetype='text/xml')


api.add_resource(Report, '/api/v1/report/')
api.add_resource(Drivers, '/api/v1/report/drivers')
