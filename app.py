import json
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask, Response
from flask import request
from model import location, weather

app = Flask(__name__)


def configure_logging():
    namespace = {}
    namespace['base_dir'] = os.path.abspath(os.path.dirname(__file__))
    namespace['logfile'] = os.path.join(namespace['base_dir'], "flask-example.log")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    rotating_file_handler = RotatingFileHandler(namespace['logfile'], maxBytes=10000, backupCount=20)
    rotating_file_handler.setLevel(logging.DEBUG)
    console_stream_handler = logging.StreamHandler()
    console_stream_handler.setLevel(logging.DEBUG if namespace.get('debug') else logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_stream_handler.setFormatter(formatter)
    rotating_file_handler.setFormatter(formatter)
    logger.addHandler(console_stream_handler)
    logger.addHandler(rotating_file_handler)
    return logger, rotating_file_handler, console_stream_handler


def read_config(p_request):
    key = '3a6c4c95fb32d6ac9c128b1fe693cbad'
    appid = ""
    loc_key = ""
    app.config.from_object('config')
    ret_value = ""
    if isinstance(p_request, str):
        return app.config[p_request]
    else:
        return ""


@app.route('/')
def main_url():
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    app.logger.info('Info')
    return read_config("INFO")


@app.route('/get_geo_by_ip', methods=['GET'])
def get_ip_geo():
    geo_access_key = read_config("geo_location_key")
    req_loc = location.RequestLocation("http://api.ipstack.com/check?",
                                       access_key=geo_access_key)
    req_loc.get_geo_url()
    location_data = req_loc.get_location_data()
    app.logger.info(location_data.__str__())
    latitude = str(location_data.get_lat())
    app.logger.info("global lat is: ", latitude)
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
#
#     r = requests.get('api.openweathermap.org/data/2.5/weather?lat=35&lon=139', )
#     resp = 200
#     return resp


# TODO change default value to config value
@app.route('/get_weather', methods=['GET'])
def get_weather():
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    geo_access_key = read_config("GEO_KEY")
    if longitude is None or latitude is None:
        req_loc = location.RequestLocation("http://api.ipstack.com/check?",
                                           access_key=geo_access_key)
        req_loc.get_geo_url()
        location_data = req_loc.get_location_data()
        app.logger.info("get the fuck out bitch")
        app.logger.info(location_data.__str__())
        latitude = str(location_data.get_lat())
        app.logger.info("global lat is: %s" % latitude)
        longitude = str(location_data.get_lon())
        app.logger.info("global lon is: %s" % longitude)
    weather_access_key = read_config("WEATHER_KEY")
    cur_weather = weather.DataForWeatherApi(lat=latitude,
                                            lon=longitude,
                                            appid=weather_access_key)
    cur_weather.get_current_weather_uri()
    weather_data = cur_weather.get_weather_data()
    resp_json = json.dumps(vars(weather_data))
    app.logger.info(resp_json)
    resp = Response(response=resp_json,
                    status=200,
                    mimetype="application/json")
    return resp


if __name__ == '__main__':
    logger, file_handler, stream_handler = configure_logging()
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.run(host='0.0.0.0',
            port=8001,
            debug=False)
