import json

import requests

from constants import *
from keys import API_KEY


class GooglePlaces(object):
    """Fetch nearby places."""

    @staticmethod
    def get(latitude=DEFAULT_LAT, longitude=DEFAULT_LONG,
            radius=DEFAULT_RANGE, place_type='bar', open_now=True,
            page_token=None):

        # Query parameters
        payload = {
            'location': f"{latitude},{longitude}",
            'radius': radius,
            'type': place_type,
            'opennow': open_now,
            'key': API_KEY,
        }

        # Fetch next page of results
        if page_token:
            payload['pagetoken'] = page_token

        req = requests.get(
            f"{NEARBY_SEARCH_URL}/{NEARBY_SEARCH_OUTPUT}", params=payload
        )

        return GooglePlaces.parse_response(req.text)

    @staticmethod
    def parse_response(json_response):
        response_dict = json.loads(json_response)
        parsed = {
            RESPONSE_RESULTS: [],
            RESPONSE_NEXT_PAGE: response_dict['next_page_token']
            if 'next_page_token' in response_dict else None,
        }

        for result in response_dict['results']:
            parsed[RESPONSE_RESULTS].append({
                RESPONSE_ID: result['place_id'],
                RESPONSE_NAME: result['name'],
                RESPONSE_ADDRESS: result['vicinity'],
                RESPONSE_LAT: result['geometry']['location']['lat'],
                RESPONSE_LONG: result['geometry']['location']['lng'],
                RESPONSE_OPEN: result['opening_hours']['open_now'],
                RESPONSE_RATING: result['rating'],
                RESPONSE_PHOTO_URL: GooglePhotos.get_url(
                    result['photos'][0]['photo_reference']
                )
            })

        return parsed


class GooglePhotos(object):
    """Fetch photos (in this context, photos of nearby places."""

    @staticmethod
    def get_url(photo_reference=None):
        return f"{PHOTOS_URL}?photoreference={photo_reference}&key={API_KEY}"
        # # Query parameters
        # payload = {
        #     'photoreference': photo_reference,
        #     'key': API_KEY,
        # }
        #
        # req = requests.get(PHOTOS_URL, params=payload)
        # return req
