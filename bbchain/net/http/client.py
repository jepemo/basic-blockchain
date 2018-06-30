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

	def register_node(self, addr, node_addr):
		url = addr + "/register_node"
		r = requests.get(url, json={
			"host": node_addr
		})
		json_resp = r.json()
		return json_resp["result"] == "OK"

	def add_block(self, addr):
		url = addr + "/add_block"
		r = requests.get(url)
		json_resp = r.json()
		if json_resp["result"] == "OK":
			return json_resp["block"]
		else:
			return None

	def add_data(self, addr, data):
		url = addr + "/add_data"
		r = requests.post(url, json={
			"data": data
		})
		json_resp = r.json()
		return json_resp["result"] == "OK"

	def get_chain(self, addr):
		url = addr + "/get_chain"
		r = requests.get(url)
		json_resp = r.json()
		chain = json_resp["chain"]
		return chain

	def sync_chain(self, addr):
		url = addr + "/sync_chain"
		r = requests.get(url)
		json_resp = r.json()
		return json_resp["result"] == "OK"
