import math
import random
import time

from flask import request
from flask_restful import Resource

from constants import *
from dao.google import GooglePlaces


class Venue(Resource):

    def __init__(self):
        # These are populated when the /venues endpoint is called in get()
        self.latitude = 0
        self.longitude = 0
        self.range = 0
        self.next_page_token = None
        self.sort_field = None
        self.sort_order = None

    def get(self):
        # Parse query parameters
        self.latitude = self.get_or_default(QUERY_PARAM_LAT, DEFAULT_LAT)
        self.longitude = self.get_or_default(QUERY_PARAM_LONG, DEFAULT_LONG)
        self.range = self.get_or_default(QUERY_PARAM_RANGE, DEFAULT_RANGE)
        self.range = float(self.range) * 1609.34  # convert miles to meters
        self.next_page_token = self.get_or_default(QUERY_PARAM_NEXT_PAGE, None)
        self.sort_field = self.get_or_default(QUERY_PARAM_SORT_FIELD,
                                              DEFAULT_SORT_FIELD)
        self.sort_order = self.get_or_default(QUERY_PARAM_SORT_ORDER,
                                              DEFAULT_SORT_ORDER)

        # Use Google to find nearby venues
        venues = GooglePlaces.get(self.latitude, self.longitude, self.range,
                                  page_token=self.next_page_token)

        # Populate extra information
        for place in venues[RESPONSE_RESULTS]:
            place[RESPONSE_TIMESTAMP] = time.time()
            place[RESPONSE_DIST] = self.calculate_distance(
                self.latitude, self.longitude,
                place[RESPONSE_LAT], place[RESPONSE_LONG]
            )

            capacity_stats = self.get_capacity_stats()
            queue_stats = self.get_queue_stats(capacity_stats)

            place[RESPONSE_MAX_CAP] = capacity_stats[0]
            place[RESPONSE_CURR_CAP] = capacity_stats[1]
            place[RESPONSE_QUEUE_LEN] = queue_stats[0]
            place[RESPONSE_QUEUE_WAIT] = queue_stats[1]

        # Sort the response
        venues[RESPONSE_RESULTS] = self.sort(venues[RESPONSE_RESULTS],
                                             self.sort_field,
                                             self.sort_order == DESCENDING)

        return venues

    @staticmethod
    def get_or_default(field, default):
        if not request.args or field not in request.args.keys():
            return default
        else:
            return request.args.get(field)

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

    @staticmethod
    def get_current_occupancy():
        return random.randint(25, 40)

    @staticmethod
    def get_capacity_stats():
        # To get some variation across places...
        curr_cap = Venue.get_current_occupancy() + random.randint(0, 40)

        # Mock max cap
        max_cap = curr_cap \
            if random.random() < 0.45 \
            else curr_cap + random.randint(1, 25)

        return max_cap, curr_cap

    @staticmethod
    def get_queue_stats(capacity_stats):
        wait_per_person = 1 + random.random()
        max_cap = capacity_stats[0]
        curr_cap = capacity_stats[1]

        queue_length = (
            int(math.ceil(curr_cap * 0.1))
            if max_cap == curr_cap
            else 0
        )
        queue_wait = round(
            wait_per_person * queue_length
            if max_cap == curr_cap
            else 0
        )

        return queue_length, queue_wait
