# -*- coding: utf-8 -*-
# bbchain - Simple extendable Blockchain implemented in Python
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

class HttpServerMiner(Server):
	def __init__(self, host, port, bc, nodes, client):
		super().__init__(host, port, bc, ["http://" + c for c in nodes] if nodes else [], client)

	def start(self):
		app = Application()
		app.router.add_route('/get_node_type', self.get_node_type)
		app.router.add_route('/add_data', self.add_data)
		app.router.add_route('/', self.help_miner)
		app.run(debug=True, host=self.host, port=self.port)

	def get_node_type(self, request):
		return request.Response(json={'type': "MINER"})

	def help_miner(self, request):
		return request.Response(json={
			"help": []
		})

	def add_data(self, request):
		return request.Response(json={"Status": "OK"})
