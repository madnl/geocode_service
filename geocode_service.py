"""
Module which contains the implementation of the geocode
lookup service.
"""

import geocode
import json
from here_provider import HereProvider
from google_maps_provider import GoogleMapsProvider
from logging_provider import ProviderWithLogging
from fallback_provider import ProviderWithFallback
from http_service import Response, json_response


with open('provider_config.json') as provider_config_file:
    provider_config = json.load(provider_config_file)

provider = ProviderWithFallback(
    primary=ProviderWithLogging(
        provider=GoogleMapsProvider(
            api_key=provider_config['google_maps']['api_key']),
        provider_name='google_maps'),

    secondary=ProviderWithLogging(
        provider=HereProvider(
            app_id=provider_config['here']['app_id'],
            app_code=provider_config['here']['app_code']),
        provider_name='here'),

    fallback_on_empty=True
)


def handle_geocode_request(request):
    address = request.get_single_param('address')
    if not address:
        response = Response.bad_request(
            'Unspecified address query parameter')
    else:
        results = provider.lookup(geocode.Query(address))
        responseObj = {
            'query': address,
            'results': [result_to_json(result) for result in results]
        }
        response = json_response(responseObj)
    return response


def result_to_json(result):
    """Convert a geocode lookup result to a JSON-representable structure"""
    return {
        'latitude': result.latitude,
        'longitude': result.longitude,
        'formatted_address': result.formatted_address
    }
