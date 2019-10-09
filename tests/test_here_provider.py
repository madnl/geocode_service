import unittest
import json
import here_provider
import geocode


class HereProviderTests(unittest.TestCase):
    def test_parse_empty_response(self):
        empty_response = json.loads("""
            {
                "Response": {
                    "View": []
                }
            }
        """)
        self.assertEqual(here_provider.extract_result(empty_response), [])

    def test_parse_result_response(self):
        with open('tests/here_single_result.json') as json_file:
            response = json.load(json_file)
            self.assertEqual(
                here_provider.extract_result(response),
                [
                    geocode.Result(
                        latitude=37.77863,
                        longitude=-122.41683,
                        formatted_address="Civic Center, San Francisco, CA, United States"
                    )
                ]
            )
