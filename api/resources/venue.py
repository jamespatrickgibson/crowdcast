import time

from flask import request
from flask_restful import Resource

from constants import *


class Venue(Resource):

    def __init__(self):
        # If location is not specified, default to UC Berkeley
        self.latitude = 37.8719
        self.longitude = 122.2585
        self.range = 10

    def get(self):
        if self.expected_query_params_exist():
            self.latitude = request.args.get(QUERY_PARAM_LAT)
            self.longitude = request.args.get(QUERY_PARAM_LONG)
            self.range = request.args.get(QUERY_PARAM_RANGE)

        return [
            {
                RESPONSE_ID: 1,
                RESPONSE_NAME: "Best bar ever",
                RESPONSE_LAT: self.latitude,
                RESPONSE_LONG: self.longitude,
                RESPONSE_DIST: 0.8,
                RESPONSE_TIMESTAMP: time.time(),
                RESPONSE_MAX_CAP: 100,
                RESPONSE_CURR_CAP: 27,
                RESPONSE_QUEUE_LEN: 0,
                RESPONSE_QUEUE_WAIT: 0,
            },
            {
                RESPONSE_ID: 2,
                RESPONSE_NAME: "In n out",
                RESPONSE_LAT: self.latitude,
                RESPONSE_LONG: self.longitude,
                RESPONSE_DIST: 1.4,
                RESPONSE_TIMESTAMP: time.time(),
                RESPONSE_MAX_CAP: 77,
                RESPONSE_CURR_CAP: 77,
                RESPONSE_QUEUE_LEN: 10,
                RESPONSE_QUEUE_WAIT: 8,
            },
            {
                RESPONSE_ID: 3,
                RESPONSE_NAME: "Another cool bar",
                RESPONSE_LAT: self.latitude,
                RESPONSE_LONG: self.longitude,
                RESPONSE_DIST: 1.6,
                RESPONSE_TIMESTAMP: time.time(),
                RESPONSE_MAX_CAP: 85,
                RESPONSE_CURR_CAP: 80,
                RESPONSE_QUEUE_LEN: 24,
                RESPONSE_QUEUE_WAIT: 30,
            },
            {
                RESPONSE_ID: 4,
                RESPONSE_NAME: "Da club",
                RESPONSE_LAT: self.latitude,
                RESPONSE_LONG: self.longitude,
                RESPONSE_DIST: 1.8,
                RESPONSE_TIMESTAMP: time.time(),
                RESPONSE_MAX_CAP: 250,
                RESPONSE_CURR_CAP: 231,
                RESPONSE_QUEUE_LEN: 30,
                RESPONSE_QUEUE_WAIT: 60,
            },
            {
                RESPONSE_ID: 5,
                RESPONSE_NAME: "Lame bar",
                RESPONSE_LAT: self.latitude,
                RESPONSE_LONG: self.longitude,
                RESPONSE_DIST: 2.5,
                RESPONSE_TIMESTAMP: time.time(),
                RESPONSE_MAX_CAP: 10,
                RESPONSE_CURR_CAP: 1,
                RESPONSE_QUEUE_LEN: 0,
                RESPONSE_QUEUE_WAIT: 0,
            },
        ]

    @staticmethod
    def expected_query_params_exist():
        """Checks that the expected query params are present on the GET call."""
        if not request.args:
            return False

        expected_params = {QUERY_PARAM_LAT, QUERY_PARAM_LONG, QUERY_PARAM_RANGE}
        diff = expected_params.difference(request.args.keys())
        return len(diff) == 0
