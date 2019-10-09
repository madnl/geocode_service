import unittest
import google_maps_provider
import json
import geocode


class GoogleMapsProviderTest(unittest.TestCase):
    def test_single_response_parse(self):
        with open('tests/google_maps_single_result.json') as response_file:
            response = json.load(response_file)
            self.assertEqual(google_maps_provider.extract_results(response), [
                geocode.Result(
                    latitude=37.7815533,
                    longitude=-122.4156427,
                    formatted_address='Civic Center, San Francisco, CA 94102, USA')
            ])
