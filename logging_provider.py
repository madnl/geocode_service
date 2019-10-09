from time import time
from geocode import Provider
import logging


class ProviderWithLogging(Provider):
    """Adds logging to an existing geocoding provider"""

    def __init__(self, provider, provider_name):
        self.provider = provider
        self.logger = logging.getLogger(f'provider.{provider_name}')

    def lookup(self, query):
        start = time()
        results = self.provider.lookup(query)
        end = time()
        self.logger.info(
            '%d results, %.2fs', len(results), end-start)
        return results
