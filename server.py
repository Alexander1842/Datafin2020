# coding: utf-8
"""
DuraLex/SedLex server.
It receives an amendment in the variable "amendment" of a POST request to /diff,
and returns an HTML diff.
"""

import http.server
import sys
import json
import re
import logging
import traceback
import time

import simul_dsr

class SimulDSRHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    server_version = "SimulDSRHTTP/0.1"

    def do_GET(self):

        self.do_POST()

    def do_POST(self):

        if self.path not in ['/simul']:
            self.send_error(400)
            return

        length = self.headers.get('content-length')
        if length:
            data = str(self.rfile.read(int(length)), 'utf-8')
        else:
            self.send_error(400)
            return

        try:
            data = json.loads(data)
        except:
            article = data

        c1 = {}
        for e in ["L2334_20","L2334_21","L2334_22","L2334_22_1"]:
            c1[e] = open(e+".txt").read()
            c2[e] = data[e]

        a = simul_dsr.Legislation(c1)
        b = simul_dsr.Legislation(c2)

        return a

if __name__ == "__main__":

    httpd = http.server.HTTPServer(('127.0.0.1', 8081), SimulDSRHTTPRequestHandler)
    sa = httpd.socket.getsockname()
    t = time.time()
    print("***", time.strftime('[%d/%b/%Y %H:%M:%S')+('%.5f]'%(t-int(t)))[1:], "***", "Serving HTTP on", sa[0], "port", sa[1], "...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        httpd.server_close()
        sys.exit(0)

# vim: set ts=4 sw=4 sts=4 et:
