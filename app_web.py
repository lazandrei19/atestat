from Interpreter import Interpreter
from VariableCtx import VariableCTX
from FunctionCtx import FunctionCTX
from antlr4 import *
from http import server, cookies
import random
import base64


class HTTPHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(open("py_tester", "r").read().encode("utf-8"))


if __name__ == '__main__':
    http_server = server.HTTPServer(('127.0.0.1', 8080), HTTPHandler)
    http_server.serve_forever()
