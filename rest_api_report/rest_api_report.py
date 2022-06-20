from flask import Flask, request, render_template, Response
from flask_restful import Resource, Api
from pathlib import Path
from flasgger import Swagger
from dicttoxml import dicttoxml
import json
from database import Driver, Time


ROOT = Path().resolve().parent
DATA_DIR = ROOT / 'Data'

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)


def create_report_dict(query, attribute=False):
    report_dict = {}
    if attribute:
        for driver in query:
            report_dict[driver.driver_id.abbreviation] = {'name': driver.driver_id.full_name,
                                                          'car': driver.driver_id.car,
                                                          'time': driver.delta_time}
    else:
        for number, driver in enumerate(query):
            number = str(number+1)
            report_dict[number] = {'number': number,
                                   'name': driver.driver_id.full_name,
                                   'car': driver.driver_id.car,
                                   'time': driver.delta_time}
    return report_dict


def create_drivers_dict(query):
    data_dict = {}
    for driver in query:
        data_dict[driver.driver_id.abbreviation] = {'abbreviation': driver.driver_id.abbreviation,
                                                    'name': driver.driver_id.full_name,
                                                    'car': driver.driver_id.car}
    return data_dict


@app.route('/report')
def show_report():
    order = request.args.get('order')
    report = Time.select(Time, Driver).join(Driver).order_by(Time.delta_time.desc()) if order == 'desc' \
        else Time.select(Time, Driver).join(Driver).order_by(Time.delta_time)
    return render_template('index.html', report=enumerate(report))


@app.route('/report/drivers/')
def show_drivers():
    driver_abr = request.args.get('driver_id')
    order = request.args.get('order')
    drivers_list = Driver.select().order_by(Driver.full_name.desc()) if order == 'desc' \
        else Driver.select().order_by(Driver.full_name)
    if driver_abr:
        driver = Time.select(Time, Driver).join(Driver).where(Driver.abbreviation == driver_abr).get()
        return f'{driver.driver_id.full_name} | {driver.driver_id.car} | {driver.delta_time}'
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
        query = Time.select(Time, Driver).join(Driver).order_by(Time.delta_time)
        report_dict = create_report_dict(query)
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
        query = Time.select(Time, Driver).join(Driver).order_by(Time.delta_time)
        drivers_dict = create_drivers_dict(query)
        if driver_abr:
            query = Time.select(Time, Driver).join(Driver).where(Driver.abbreviation == driver_abr)
            report_dict = create_report_dict(query, True)
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


if __name__ == '__main__':
    app.run(debug=True)
