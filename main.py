#!/usr/bin/env python
# encoding=utf-8
import sys
import os
import BaseHTTPServer
from urlparse import urlparse
import json
from server import *

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):        
        path = self.path
        
        query = urlparse(path).query.split('&')

        title = query[0].split('=')[1]
        author = query[1].split('=')[1]

        print title, author
        # title = '出租车发票'
        # author = '吴质'

        # First, send a 200 OK response.
        self.send_response(200)

        # Then send headers.
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        result = main(title, author)

        # Now, write the response body.
        self.wfile.write(json.dumps(result))

if __name__ == '__main__':
    server_address = ('', 8000)  # Serve on all addresses, port 8000.
    server = BaseHTTPServer.HTTPServer(server_address, RequestHandler)
    server.serve_forever()