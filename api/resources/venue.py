import math
import time

from flask import request
from flask_restful import Resource

from constants import *
from dao.google import GooglePlaces


class Venue(Resource):

    def __init__(self):
        # If location is not specified, default to UC Berkeley
        self.latitude = DEFAULT_LAT
        self.longitude = DEFAULT_LONG
        self.range = DEFAULT_RANGE

    def get(self):
        if self.expected_query_params_exist():
            self.latitude = request.args.get(QUERY_PARAM_LAT)
            self.longitude = request.args.get(QUERY_PARAM_LONG)
            # Convert miles to meters
            self.range = float(request.args.get(QUERY_PARAM_RANGE)) * 1609.34

        nearby = GooglePlaces.get(self.latitude, self.longitude, self.range,
                                  open_now=False)

        # Mock the missing data
        for place in nearby[RESPONSE_RESULTS]:
            place[RESPONSE_TIMESTAMP] = time.time()
            place[RESPONSE_DIST] = self.calculate_distance(
                self.latitude, self.longitude,
                place[RESPONSE_LAT], place[RESPONSE_LONG]
            )
            place[RESPONSE_MAX_CAP] = 100
            place[RESPONSE_CURR_CAP] = 89
            place[RESPONSE_QUEUE_LEN] = 10
            place[RESPONSE_QUEUE_WAIT] = 15

        nearby[RESPONSE_RESULTS] = self.sort(nearby[RESPONSE_RESULTS])

        return nearby

    @staticmethod
    def expected_query_params_exist():
        """Checks that the expected query params are present on the GET call."""
        if not request.args:
            return False

        expected_params = {QUERY_PARAM_LAT, QUERY_PARAM_LONG, QUERY_PARAM_RANGE}
        diff = expected_params.difference(request.args.keys())
        return len(diff) == 0

    @staticmethod
    def calculate_distance(lat1, long1, lat2, long2):
        R = 6371e3
        phi1 = math.radians(float(lat1))
        phi2 = math.radians(float(lat2))
        delta_phi = math.radians(float(lat1) - float(lat2))
        delta_lambda = math.radians(float(long1) - float(long2))
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c / 1609.34  # convert from meters to miles

    @staticmethod
    def sort(places, sort_field=RESPONSE_DIST, sort_desc=False):
        return sorted(places, key=lambda i: i[sort_field], reverse=sort_desc)
