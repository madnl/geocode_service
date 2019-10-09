import geocode
import json
import urllib.parse as urlparse
import urllib.request as request
from urllib.error import URLError
from http_client import perform_get


class HereProvider(geocode.Provider):
    """Implementation for a geocode provider based on the HERE service.

    See: https://developer.here.com/documentation/geocoder/topics/quick-start.html
    """

    def __init__(self, app_id, app_code):
        self.app_id = app_id
        self.app_code = app_code

    def lookup(self, query):
        try:
            response_text = perform_get(
                domain='geocoder.api.here.com',
                path='/6.2/geocode.json',
                query_params={
                    'app_id': self.app_id,
                    'app_code': self.app_code,
                    'searchtext': query.address
                })
        except URLError as ex:
            raise geocode.ProviderError(ex)
        response = json.loads(response_text)
        return extract_result(response)


def extract_result(response):
    view_section = response['Response']['View'] or []
    search_result = next(
        (view for view in view_section if view.get('_type', None) == 'SearchResultsViewType'), None)
    if not search_result:
        return []
    return list((convert_result(result) for result in search_result['Result']))


def convert_result(result):
    pos = result['Location']['DisplayPosition']
    return geocode.Result(
        latitude=pos['Latitude'],
        longitude=pos['Longitude'],
        formatted_address=result['Location']['Address']['Label'])
