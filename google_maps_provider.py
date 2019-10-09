import geocode
from http_client import perform_get
import json
from urllib.error import URLError


class GoogleMapsProvider(geocode.Provider):
    """Implementation for the geocode provider API based on the Google Maps API.

    See https://developers.google.com/maps/documentation/geocoding/start
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def lookup(self, query):
        try:
            response_str = perform_get(
                domain='maps.googleapis.com',
                path='/maps/api/geocode/json',
                query_params={
                    'key': self.api_key,
                    'address': query.address})
        except URLError as ex:
            raise geocode.ProviderError(ex)
        response = json.loads(response_str)
        return extract_results(response)


def extract_results(response):
    if (response['status'] != 'OK'):
        raise geocode.ProviderError(
            f'Google Maps API returned JSON status {response["status"]}')
    return list((convert_result(result) for result in response['results']))


def convert_result(response_result):
    location = response_result['geometry']['location']
    return geocode.Result(
        latitude=location['lat'],
        longitude=location['lng'],
        formatted_address=response_result['formatted_address'])
