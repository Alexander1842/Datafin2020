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

        if self.path not in ['/simul_dsr']:
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
        c2 = {}
        for e in ["L2334_20","L2334_21","L2334_22","L2334_22_1"]:
            c1[e] = open(e+".txt").read()
            c2[e] = data[e] if e in data else c1[e]

        open('L2334_21-modifié.txt', 'w').write(c2['L2334_21'])

        a = simul_dsr.Legislation(c1)
        b = simul_dsr.Legislation(c2)

        db_raw = simul_dsr.get_dict_db('dgcl_2019.csv')
        db_communes = []

        for e in db_raw:
            db_communes.append(simul_dsr.Commune(db_raw,e))

        d_c = {"nat_pfi_m_10k":856.050899}

        s = simul_dsr.Simulation(db_communes,a,b,d_c)
        o,n = s._simulation_generale()
        syn = s._generer_synthese(o,n)

        json_syn = json.dumps(syn, sort_keys=True, indent=None, ensure_ascii=False, separators=(',', ':'))

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(bytes(json_syn,'utf-8')))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(json_syn, 'utf-8'))

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
