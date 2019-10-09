import urllib.parse as urlparse
import urllib.request as request


def perform_get(domain, path, query_params=None, protocol='https'):
    """Simple way of performing a get request"""
    parts = (protocol, domain, path, '', build_query(query_params or {}), '')
    url = urlparse.urlunparse(parts)
    with request.urlopen(url) as response:
        return response.read()


def build_query(params):
    pairs = (f"{urlparse.quote(name)}={urlparse.quote(value)}"
             for name, value in params.items())
    return '&'.join(pairs)
