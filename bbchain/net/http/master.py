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

import queue
import sys
from aiohttp import web
from bbchain.net.network import SenderReceiver
from bbchain.settings import logger
from bbchain.net.http.base import HttpServerBase

class HttpServerMaster(HttpServerBase):
    def __init__(self, host, port, bc, master_nodes):
        HttpServerBase.__init__(host, port, bc, master_nodes, "MASTER")

    async def connect(self, request):
        info = await request.json()
        node_host = info['host']
        node_type = info['type']

        logger.debug("Adding Node {0} of type {1}".format(node_host, node_type))
        if node_type == "MASTER" and node_host not in self.masters:
            self.masters.append(node_host)
        elif node_type == "MINER" and node_host not in self.miners:
            self.miners.append(node_host)

    def _add_data(self, last_hash, data):
        if not self.miners or len(self.miners) == 0:
            logger.error("This node is not connected to any miner.")
            return

        for m in self.miners:
            self.client.send_data_to_miner(m, last_hash, data)

    def _get_last_hash(self):
        return self.bchain.last_hash

    async def add_data(self, request):
        content = await request.json()
        data = content["data"]
        last_hash = self._get_last_hash()
        self._add_data(last_hash, data)
        return web.json_response({'result': "OK"})
    
    async def add_block(self, request):
        content = await request.json()
        block = content["block"]

        self.bchain.add_checked_block(block)
        return web.json_response({'result': "OK"})

    async def get_blocks(self, request):
        q = request.rel_url.query
        count = int(q['count']) if 'count' in q else 10
        pointer = q['from_hash'] if 'from_hash' in q else self.bchain.last_hash

        chain = []
        while pointer and count > 0:
            block = self.bchain.db.get_block(pointer)
            chain.append(block.to_dict())
            #pointer = block.prev_block_hash
            pointer = block.next_block_hash
            count -= 1

        return web.json_response({ 'chain': chain})

    def get_help(self):
        return {
            "help": [
                "get_blocks",
            ]
        }

    def start(self):
        app = web.Application()
        app.add_routes([web.post('/connect', self.connect),
                        web.post('/add_data', self.add_data),
                        web.post('/add_block', self.add_block),
                        web.get('/get_nodes', self.get_nodes),
                        web.get('/get_node_type', self.get_node_type),
                        web.get('/get_blocks', self.get_blocks),
                        web.get('/', self.help_node)])

        web.run_app(app, host=self.host, port=self.port)
