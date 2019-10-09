import http.server
import socketserver
import json
import geocode
import logging
from http_service import Request, Response
from geocode_service import handle_geocode_request

logging.basicConfig(level=logging.INFO)

PORT = 8000

# Listening on all network interfaces on the given port
listening_address = ("", PORT)

LOOKUP_REQUEST_PATH = '/geo_lookup.json'


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        request = Request(self.path, method='GET')
        if (request.path != LOOKUP_REQUEST_PATH):
            response = Response.not_found(request.path)
        else:
            try:
                response = handle_geocode_request(request)
            except Exception as ex:
                logging.exception(ex)
                response = Response.server_error()
        self.send_response(response.status_code)
        body = response.encoded_body()
        headers = dict(response.headers)
        headers['Content-Length'] = str(len(body))
        for header_name, header_value in headers.items():
            self.send_header(header_name, header_value)
        self.end_headers()
        self.wfile.write(body)


logging.info('Initializing TCP server')
with socketserver.TCPServer(listening_address, RequestHandler) as httpd:
    logging.info('Starting server on port %s', httpd.server_address)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    logging.info('Server will shut down')
    httpd.shutdown()
    httpd.server_close()
