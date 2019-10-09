import geocode
import logging

fallback_logger = logging.getLogger('provider.fallback')


class ProviderWithFallback(geocode.Provider):
    """Implements a geocode provider by delegating the lookup request
    to a primary underlying provider and then to a secondary if the
    primary fails"""

    def __init__(self, primary, secondary, fallback_on_empty=True, log_handled_exception=True):
        """
        primary - the primary provider
        secondary - the secondary provider
        fallback_on_empty - should we call the secondary provider if the primary succeedes
            but returns an empty list of results
        log_handled_exception - should we log exceptions when we continue with alternate results
        """
        self.primary = primary
        self.secondary = secondary
        self.fallback_on_empty = fallback_on_empty
        self.log_handled_exception = log_handled_exception

    def lookup(self, query):
        primary_results = None
        try:
            primary_results = self.primary.lookup(query)
            # if the primary provider was successful and returned a non-empty
            # list, return the primary's results
            # otherwise, if the list is empty and we chose to fallback on
            # empty results, do not return and continue with the secondary provider
            if primary_results or not self.fallback_on_empty:
                return primary_results
        except Exception as primary_ex:
            # do not crash on the primary's exception, but log it for observability
            if self.log_handled_exception:
                fallback_logger.exception(primary_ex)
        try:
            return self.secondary.lookup(query)
        except Exception as secondary_ex:
            # At this point the first provider either failed or returned no
            # results and the second provider failed. If the first provider
            # returned, but the result list was empty, we return the empty list,
            # otherwise we let the second exception through
            if primary_results is not None:
                if self.log_handled_exception:
                    fallback_logger.exception(secondary_ex)
                return primary_results
            else:
                raise secondary_ex
