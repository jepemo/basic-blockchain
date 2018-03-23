# -*- coding: utf-8 -*-
# bbchain - Basic cryptocurrency, based on blockchain, implemented in Python
#
# Copyright (C) 2017-present Jeremies Pérez Morata
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import socketserver
import sys
from http.server import BaseHTTPRequestHandler
from bbchain.net.network import Server

class BaseHandler(BaseHTTPRequestHandler):
	def __init__(self, request, client_address, server):
		BaseHTTPRequestHandler.__init__(self, request, client_address, server)
		self.get_actions = {}
		self.post_actions = {}
		
	def _set_headers(self, code=200):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		
	def do_GET(self):
		try:
			action = "get_blocks"
			handler = self.get_actions[action]
			params = {}
			
			result = handler(params)
			
			self._set_headers()
			self.wfile.write(json.dumps(result).encode('utf-8'))
		except Exception as ex:
			print("Error:", sys.exc_info()[0])
			error = { "error": str(ex) }
			self._set_headers(code=400)
			self.wfile.write(json.dumps(error).encode('utf-8'))
		
	def _add_get(self, action, handler):
		self.get_actions[action] = handler

class MasterHandler(BaseHandler):
	def __init__(self, request, client_address, server):
		BaseHandler.__init__(self, request, client_address, server)
		self._add_get("get_blocks", self.get_blocks)
		
	def get_blocks(self, params):
		return {}
		
class MinerHandler(BaseHandler):
	def __init__(self, request, client_address, server):
		BaseHTTPRequestHandler.__init__(self, request, client_address, server)
	

class HttpServer(Server):
	def __init__(self, host, port, bc):
		self.bchain = bc
		self.host = host
		self.port = port
		
	def _start_server(self, handler):
		with socketserver.TCPServer((self.host, self.port), handler) as httpd:
			print("Serving at port", self.port)
			httpd.serve_forever()	
		
	def start_master(self):
		#handler = http.server.SimpleHTTPRequestHandler
		handler = MasterHandler
		self._start_server(handler)
		
		
			
	def start_miner(self):
		pass