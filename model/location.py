import json
import urllib

import requests


class Location:

    # initialize the class with geo coordinates

    def __init__(self, lat, lon, city, locale):
        self.lat = lat
        self.lon = lon
        self.city = city
        self.locale = locale

    def get_lon(self):
        return self.lon

    def get_lat(self):
        return self.lat

    def is_city_none(self):
        return self.city is None

    def get_locale(self):
        if self.locale is not None:
            return self.locale
        return False

    def __str__(self) -> str:
        return str(self.lat) + str(self.lon) + str(self.city) + str(self.locale)


class RequestLocation(object):

    def __init__(self, base_url, access_key, f_url=""):
        self.base_url = base_url
        self.access_key = access_key
        self.f_url = f_url

    def get_geo_url(self):
        l_base_url = self.base_url
        access_key = self.access_key
        get_var = {'access_key': access_key}
        full_url = l_base_url + urllib.parse.urlencode(get_var)
        print("full url is: ", full_url)
        self.f_url = full_url
        return self.f_url

    def get_location_data(self):
        # global latitude
        # global longitude
        # global city
        if len(self.f_url) > 0:
            geo_req = requests.get(self.f_url)
            geo_json = geo_req.json()
            latitude = geo_json['latitude']
            longitude = geo_json['longitude']
            city = geo_json['city']
            country_code = geo_json['country_code']
            location = Location(latitude, longitude, city, country_code)
            return location
        else:
            return "url is empty"

        # latitude = geo_json['latitude']
        # longitude = geo_json['longitude']
        # city = geo_json['city']
        # country_code = json['country_code']
        # location = Location(latitude, longitude, city, country_code)
