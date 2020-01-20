from flask import Blueprint, request, make_response, jsonify
from influxdb import InfluxDBClient

from requests import post
from datetime import datetime

temp_blueprint = Blueprint('temperatures', __name__)
db_temp_client = InfluxDBClient(host="influxdb", 
                                port=8086, 
                                username='admin', 
                                password='admin',
                                database='temperatures')

temp_insert_msg_body = [
    {
        "measurement": "temperatures",
        "tags": {
            "host": "data_server",
            "id" : None
        },
        "time": None, 
        "fields": {
            "value": None
        }
    }
]

def add_temp(temp_reading):
    insert_query = temp_insert_msg_body
    insert_query[0]["time"] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    insert_query[0]["fields"]["value"] = temp_reading

    db_temp_client.write_points(insert_query)
    
    post('http://central-server/fire_alarm/{}/temp'.format(temp_insert_msg_body[0]['tags']['id']),
        json = {'temp' : str(temp_reading)})
    

def get_temps():
    measurements    = []
    result          = db_temp_client.query('SELECT value FROM temperatures;')

    for element in result.raw['series']:
        for value in element['values']:
            measurements.append(value)

    return measurements


@temp_blueprint.route('/temp', methods = ['POST', 'GET'])
def attend_temperatures():
    if request.method == 'POST':
        if not request.json or not 'msg' in request.json:
            return make_response(jsonify({'error' : 'Bad Request'}), 400)
        else:
            add_temp(request.json['msg'])
            return make_response(jsonify({'success': True}), 200)

    if request.method == 'GET':
        return make_response(jsonify({ 'data' : get_temps() }), 200)

@temp_blueprint.route('/create_temp_model', methods = ['POST'])
def create_temp_model():
    result = post("http://central-server:8000/fire_alarm/")
    temp_insert_msg_body[0]['tags']['id'] = result.json()['_id']

    return make_response(jsonify({"status" : "OK"}), 200)