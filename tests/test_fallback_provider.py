import unittest
import geocode
from unittest.mock import MagicMock
from fallback_provider import ProviderWithFallback


class ProviderWithFallbackTest(unittest.TestCase):
    def setUp(self):
        self.primary_results = [geocode.Result(
            latitude=1, longitude=1, formatted_address='1')]
        self.secondary_results = [geocode.Result(
            latitude=2, longitude=2, formatted_address='2')]
        self.query = geocode.Query(address='foo')

    def test_primary_has_priority(self):
        primary = geocode.Provider()
        primary.lookup = MagicMock(return_value=self.primary_results)
        secondary = geocode.Provider()
        secondary.lookup = MagicMock(return_value=self.secondary_results)
        provider = ProviderWithFallback(
            primary, secondary, fallback_on_empty=True)
        results = provider.lookup(self.query)
        self.assertEqual(results, self.primary_results)

    def test_empty_primary_returned_if_not_fallback_on_empty(self):
        primary = geocode.Provider()
        primary.lookup = MagicMock(return_value=[])
        secondary = geocode.Provider()
        secondary.lookup = MagicMock(return_value=self.secondary_results)
        provider = ProviderWithFallback(
            primary, secondary, fallback_on_empty=False)
        results = provider.lookup(self.query)
        self.assertEqual(results, [])

    def test_secondary_returned_if_fallback_on_empty(self):
        primary = geocode.Provider()
        primary.lookup = MagicMock(return_value=[])
        secondary = geocode.Provider()
        secondary.lookup = MagicMock(return_value=self.secondary_results)
        provider = ProviderWithFallback(
            primary, secondary, fallback_on_empty=True)
        results = provider.lookup(self.query)
        self.assertEqual(results, self.secondary_results)

    def test_secondary_returned_if_primary_fails(self):
        primary = geocode.Provider()
        primary.lookup = MagicMock(side_effect=Exception('1'))
        secondary = geocode.Provider()
        secondary.lookup = MagicMock(return_value=self.secondary_results)
        provider = ProviderWithFallback(
            primary, secondary, fallback_on_empty=False, log_handled_exception=False)
        results = provider.lookup(self.query)
        self.assertEqual(results, self.secondary_results)

    def test_primary_empty_results_if_secondary_fails(self):
        primary = geocode.Provider()
        primary.lookup = MagicMock(return_value=[])
        secondary = geocode.Provider()
        secondary.lookup = MagicMock(side_effect=Exception('2'))
        provider = ProviderWithFallback(
            primary, secondary, fallback_on_empty=True, log_handled_exception=False)
        results = provider.lookup(self.query)
        self.assertEqual(results, [])

    def test_raise_secondary_exception_if_both_fail(self):
        primary = geocode.Provider()
        primary_ex = Exception('1')
        primary.lookup = MagicMock(side_effect=primary_ex)
        secondary = geocode.Provider()
        secondary_ex = Exception('2')
        secondary.lookup = MagicMock(side_effect=secondary_ex)
        provider = ProviderWithFallback(
            primary, secondary, fallback_on_empty=False, log_handled_exception=False)
        with self.assertRaises(Exception) as exception_context:
            provider.lookup(self.query)
        self.assertEqual(exception_context.exception, secondary_ex)
