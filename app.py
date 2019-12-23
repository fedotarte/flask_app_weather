import json

from flask import Flask, Response
from flask import request
import configparser
from model import location, weather

app = Flask(__name__)


def read_config():
    key = '3a6c4c95fb32d6ac9c128b1fe693cbad'
    appid = ""
    loc_key = ""
    parser = configparser.ConfigParser()
    try:
        parser.read('config.ini')
        for sect in parser.sections():
            print('Section: %s' % sect)
            for k, v in parser.items(sect):
                print(' {} = {}'.format(k, v))
                if k == 'locationkey':
                    loc_key = v
                elif k == 'accesskey':
                    appid = v
                else:
                    print("nothing found")
    except OSError as e:
        print(e)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get_geo_by_ip', methods=['GET'])
def get_ip_geo():
    req_loc = location.RequestLocation("http://api.ipstack.com/check?", access_key=loc_key)
    req_loc.get_geo_url()
    location_data = req_loc.get_location_data()
    print(location_data.__str__())
    latitude = str(location_data.get_lat())
    print("global lat is: ", latitude)
    longitude = str(location_data.get_lon())
    return "i got the coords" + str(latitude) + str(longitude)


# @app.route('get_geo_by_coordinates', methods=['GET'])
# def get_cooerd_geo():
#     resp = None
#     longitude = request.args.get('longitude')
#     latitude = request.args.get('longitude')
#     params = [longitude, latitude]
#     for item in params:
#         if item is None:
#             resp = 400
#             return resp
#     # todo get the json weather and return it to client
#     r = requests.get('api.openweathermap.org/data/2.5/weather?lat=35&lon=139', )
#     resp = 200
#     return resp

@app.route('/get_weather', methods=['GET'])
def get_weather():
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    if longitude is None or latitude is None:
        req_loc = location.RequestLocation("http://api.ipstack.com/check?",
                                           access_key="7761abaed364fdc2bb47d511bfdd9a3f")
        req_loc.get_geo_url()
        location_data = req_loc.get_location_data()
        print(location_data.__str__())
        latitude = str(location_data.get_lat())
        print("global lat is: %s" % latitude)
        longitude = str(location_data.get_lon())
        print("global lon is: %s" % longitude)
    cur_weather = weather.DataForWeatherApi(lat=latitude, lon=longitude, appid='3a6c4c95fb32d6ac9c128b1fe693cbad')
    cur_weather.get_current_weather_uri()
    weather_data = cur_weather.get_weather_data()
    resp_json = json.dumps(vars(weather_data))
    print(resp_json)
    resp = Response(response=resp_json,
                    status=200,
                    mimetype="application/json")
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
