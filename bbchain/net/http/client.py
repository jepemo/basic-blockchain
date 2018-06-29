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

import requests
import time
from bbchain.net.network import Client
from bbchain.settings import logger

class HttpClient(Client):
	def __init__(self):
		pass

	"""
	def get_node_type(self, addr):
		r = requests.get(addr + "/get_node_type")
		json_resp = r.json()
		return json_resp["type"]

	def get_nodes(self, addr):
		r = requests.get(addr + "/get_nodes")
		json_resp = r.json()
		return json_resp["masters"], json_resp["miners"]

	def connect(self, addr, node_addr, node_type):
		r = requests.post(addr + "/connect", json={
			'host': node_addr,
			'type': node_type
		})
		json_resp = r.json()
		return json_resp["result"] == "OK"

	def add_data(self, nodes, data):
		if not nodes or len(nodes) == 0:
			logger.error("You need to specify a master node")
			return False

		# We only select one master node
		master = nodes[0]
		master_addr = "http://" + master + "/add_data"

		logger.debug("Sending {0} bytes of data to {1}".format(len(data), master_addr))

		r = requests.post(master_addr, json={
			"data": data
		})
		json_resp = r.json()
		return json_resp["result"] == "OK"

	def send_data_to_miner(self, addr, last_hash, data):
		url = addr + "/add_data"
		r = requests.post(url, json={
			"last_hash": last_hash,
			"data": data
		})
		json_resp = r.json()
		return json_resp["result"] == "OK"

	def send_block_to_master(self, addr, block):
		url = addr + "/add_block"
		r = requests.post(url, json={
			"block": block
		})
		json_resp = r.json()
		return json_resp["result"] == "OK"

	def get_bchain_from_master(self, addr, last_hash):
		actual_hash = last_hash
		url = addr + "/get_blocks"
		blocks = []

		while True:
			r = requests.get(url, json={
				'from_hash' : actual_hash,
			})

			json_resp = r.json()
			chain = json_resp["chain"]
			if chain == []:
				break
			else:
				blocks.extend(chain)
				actual_hash = chain[-1]['hash']
				time.sleep(1)

		return blocks
	"""
	
	def get_chain(self, addr):
		url = addr + "/get_chain"
		r = requests.get(url)
		json_resp = r.json()
		chain = json_resp["chain"]

		return chain
