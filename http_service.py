"""
Data objects useful for implementing an HTTP service.
"""
from urllib.parse import urlparse, parse_qs
import json


class StatusCodes:
    """Numeric constants for specifying HTTP status codes"""
    OK = 200
    NOT_FOUND = 404
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500


class CommonHeaders:
    """Common HTTP header names"""
    ContentType = 'Content-Type'


class ContentTypes:
    """Common values to indicate content types.

    Useful for specifying values for Accept or Content-Type headers"""
    JSON = 'application/json'
    PlainText = 'text/plain'


class TextEncodings:
    """Common text encoding schemas"""
    UTF8 = 'utf-8'


class Response:
    """Representation of an HTTP response"""

    def __init__(self, body, status_code=StatusCodes.OK, content_type=ContentTypes.PlainText, encoding=TextEncodings.UTF8, headers=None):
        self.body = body
        self.status_code = status_code
        self.headers = headers or {}
        self.encoding = encoding
        self.headers['Content-Type'] = f'{content_type}; charset={encoding}'

    def encoded_body(self):
        return self.body.encode(self.encoding)

    @staticmethod
    def plain_text(body, status_code=StatusCodes.OK):
        return Response(body=body, status_code=status_code, content_type=ContentTypes.PlainText)

    @staticmethod
    def not_found(path_name):
        return Response.plain_text(
            body=f'Not found: {path_name}\n',
            status_code=StatusCodes.NOT_FOUND)

    @staticmethod
    def bad_request(info):
        return Response.plain_text(status_code=StatusCodes.BAD_REQUEST, body=f'Bad request: {info}\n')

    @staticmethod
    def server_error():
        return Response.plain_text(
            status_code=StatusCodes.INTERNAL_SERVER_ERROR,
            body='Internal Server Error\n')


def json_response(data, status_code=StatusCodes.OK, encoding=TextEncodings.UTF8, headers=None):
    """Creates a response from a JSON serializable object"""
    return Response(
        body=json.dumps(data, ensure_ascii=True, indent=2) + '\n',
        status_code=status_code,
        encoding=encoding,
        headers=headers,
        content_type=ContentTypes.JSON)


class Request:
    """Simplified representation of an HTTP request"""

    def __init__(self, raw_url, method):
        parsed_url = urlparse(raw_url)
        self.path = parsed_url.path
        self.query = parsed_url.query
        self.query_params = parse_qs(self.query)
        self.method = method

    def get_single_param(self, name, default=None):
        """Get the value for the parameter with the given name.

        If the param was not specified, the result defaults to None"""
        values = self.query_params.get(name, None)
        if not values or len(values) == 0:
            return default
        return values[0]
