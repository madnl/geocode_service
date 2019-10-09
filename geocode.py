"""
Module providing data modelling objects and the provider
interface for the geocoding problem space
"""


class Result:
    """The result of a geocode lookup"""

    def __init__(self, latitude, longitude, formatted_address):
        self.latitude = latitude
        self.longitude = longitude
        self.formatted_address = formatted_address

    def __eq__(self, other):
        if not isinstance(other, Result):
            return False
        return (self.latitude == other.latitude and
                self.longitude == other.longitude and
                self.formatted_address == other.formatted_address)


class Query:
    """Data representation for a geocode query"""

    def __init__(self, address):
        self.address = address


class Provider:
    """Base interface for geocode providers"""

    def lookup(self, query):
        """"Perform a lookup given the specified query

        Returns:
        A (possibly empty) array of lookup results

        Throws:
        LookupFailure - if something is logically wrong with the query
        ProviderError - if the request was successful but we cannot parse it
        UrlError - if something is wrong at the network level
        """
        pass


class ProviderError(Exception):
    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason
