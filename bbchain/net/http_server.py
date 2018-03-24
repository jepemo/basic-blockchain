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

import sys
from japronto import Application
from bbchain.net.network import Server

class HttpServer(Server):
	def __init__(self, host, port, bc):
		self.bchain = bc
		self.host = host
		self.port = port
	
	def help_master(self, request):
		return request.Response(json={
			"help": [
				"get_blocks",
			]
		})
	def help_miner(self, request):
		return request.Response(json={
			"help": []	
		})
			
	def get_blocks(self, request):
		count = request.query['count'] if 'count' in request.query else 10
		pointer = request.query['from_hash'] if 'from_hash' in request.query else self.bc.last_hash
		
		#print(request.query)
		return request.Response(json={ 'text': 'Hello world!'})	
		
	def start_master(self):
		app = Application()
		app.router.add_route('/get_blocks', self.get_blocks)
		app.router.add_route('/', self.help_master)
		app.run(debug=True, host=self.host, port=self.port)
			
	def start_miner(self):
		app = Application()
		app.router.add_route('/', self.help_miner)
		app.run(debug=True, host=self.host, port=self.port)
