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

class Client:
	def __init__(self):
		pass

class Server:
	def __init__(self, host, port, bc, nodes, client):
		self.bchain = bc
		self.host = host
		self.port = port
		self.client = client
		self.masters = []
		self.miners = []

		self._init_nodes(nodes)
		# print(self.masters, self.miners)

	def start():
		raise Exception("Not implemented exception")

	def _init_nodes(self, nodes):
		for node in nodes:
			ntype = self.client.get_node_type(node)
			if ntype == "MASTER":
				self.masters.append(node)
			elif ntype == "MINER":
				self.miners.append(node)
			else:
				print("Unknown node:", node, "with type", ntype)
