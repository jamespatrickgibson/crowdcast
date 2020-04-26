# Sorting
ASCENDING = 'asc'
DESCENDING = 'desc'

# Default values
DEFAULT_LAT = 37.871853
DEFAULT_LONG = -122.258423
DEFAULT_RANGE = 5  # miles
DEFAULT_SORT_FIELD = 'distance'
DEFAULT_SORT_ORDER = 'asc'  # or 'desc'

# Query parameters
QUERY_PARAM_LAT = 'latitude'
QUERY_PARAM_LONG = 'longitude'
QUERY_PARAM_RANGE = 'range'
QUERY_PARAM_SORT_FIELD = 'sort_by'
QUERY_PARAM_SORT_ORDER = 'sort_order'
QUERY_PARAM_NEXT_PAGE = 'next_page_token'

# Response fields
RESPONSE_RESULTS = 'results'
RESPONSE_ID = 'id'
RESPONSE_NAME = 'name'
RESPONSE_ADDRESS = 'address'
RESPONSE_LAT = 'latitude'
RESPONSE_LONG = 'longitude'
RESPONSE_DIST = 'distance'
RESPONSE_OPEN = 'open_now'
RESPONSE_RATING = 'rating'
RESPONSE_PHOTO_URL = 'photo_url'
RESPONSE_TIMESTAMP = 'timestamp'
RESPONSE_MAX_CAP = 'max_capacity'
RESPONSE_CURR_CAP = 'current_capacity'
RESPONSE_QUEUE_LEN = 'queue_length'
RESPONSE_QUEUE_WAIT = 'queue_wait_time'
RESPONSE_NEXT_PAGE = 'next_page_token'

# Google shit
NEARBY_SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch'
NEARBY_SEARCH_OUTPUT = 'json'
PHOTOS_URL = 'https://maps.googleapis.com/maps/api/place/photo'
