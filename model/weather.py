import urllib.parse as urlparse
from urllib.parse import urlencode

import requests


class WeatherData:
    def __init__(self, weather_description,
                 main_temp,
                 main_humidity,
                 wind_speed,
                 location_name):
        self.weather_description = weather_description
        self.main_temp = main_temp
        self.main_humidity = main_humidity
        self.wind_speed = wind_speed
        self.location_name = location_name


class DataForWeatherApi:
    def __init__(self, lat, lon, appid):
        self.lat = lat
        self.lon = lon
        self.appid=appid
        self.f_url = ""
        print("weather with: ", self.lat, self.lon)
        pass

    # 55.5877
    # 37.6428
    def get_current_weather_uri(self):
        get_weather_url = ' http://api.openweathermap.org/data/2.5/weather'
        params = {
            'lang': 'ru',
            'units': 'metric',
            'appid': '',
            'lat': '51.509865',
            'lon': '-0.118092'
        }
        if self.lat.__len__() > 0 and \
           self.lat.__len__() > 0 and \
            self.appid.__len__() > 0:
            print("asserted")
            params['lat'] = self.lat
            print("changed 1")
            params['lon'] = self.lon
            print("changed 2")
            params["appid"] = self.appid
        url_parts = list(urlparse.urlparse(get_weather_url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        self.f_url = urlparse.urlunparse(url_parts)
        return str(self.f_url)

    def get_weather_data(self):

        # global latitude
        # global longitude
        # global city
        if len(self.f_url) > 0:
            geo_req = requests.get(self.f_url)
            weather_json = geo_req.json()
            print(weather_json)
            weather_description = weather_json['weather'][0]['description']
            main_temp = weather_json['main']['temp']
            main_humidity = weather_json['main']['humidity']
            wind_speed = weather_json['wind']['speed']
            location_name = weather_json['name']
            weather_data = WeatherData(weather_description,
                                       main_temp,
                                       main_humidity,
                                       wind_speed,
                                       location_name)
            return weather_data
        else:
            return "url is empty"
