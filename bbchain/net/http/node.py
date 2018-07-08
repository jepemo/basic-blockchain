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

from bbchain.net.http.client import HttpClient
from bbchain.settings import logger
from aiohttp import web

class HttpNode:
    def __init__(self, host, port, bc, hosts):
        self.host = host
        self.port = port
        self.bchain = bc
        self.client = HttpClient()
        self.hosts = hosts
        self.max_data = 1

    async def help(self, request):
        return web.json_response({
            "help": [
                { "/add_data" : "Adds data to the node buffer, waiting to be mined."},
                { "/add_block" : "Mine and create a block"},
                { "/get_chain" : "Retrieve the chain"},
                { "/sync_chain" : "Synchronizes the chain (the longest)"},
                { "/register_node" : "Connects to another node"},
            ]
        })

    # def check_add_block(self):
    #     if len(self.bchain.current_data) == self.max_data:
    #         self.bchain.add_block()

    async def add_data(self, request):
        # self.check_add_block()
        json_resp = await request.json()
        data = json_resp["data"]
        self.bchain.add_data(data)
        return web.json_response({
            "result": "OK"
        })

    async def add_block(self, request):
        new_block = self.bchain.add_block()
        return web.json_response({
            "result": "OK",
            "block": new_block.to_dict()
        })

    def _get_all_blocks(self):
        chain = []
        last_hash = self.bchain.last_hash
        while last_hash:
            block = self.bchain.get_block(last_hash)
            chain.append(block)
            last_hash = block.prev_block_hash

    async def get_chain(self, request):
        chain = self._get_all_blocks()
        return web.json_response({
            "result": "OK",
            "count": len(chain),
            "chain": [b.to_dict() for b in chain]
        })

    async def register_node(self, request):
        info = await request.json()
        node_host = info['host']

        if node_host not in self.hosts:
            self.hosts.append(node_host)

        return web.json_response({
            "result": "OK"
        })

    async def sync_chain(self, request):
        chains = {}
        max_chain_length = 0
        for host in self.hosts:
            chain = self.client.get_chain(host)
            chain_length = len(chain)
            chains[chain_length] = chain
            if max_chain_length < chain_length:
                max_chain_length = chain_length

        selected_chain = chains[max_chain_length]
        actual_chain = self._get_all_blocks()

        update_chain = len(selected_chain) > len(actual_chain)
        if update_chain:
            self.bchain.clean_db()
            for block in reversed(selected_chain):
                self.bchain.add_checked_block(block)

        size = len(self._get_all_blocks())
        return web.json_response({
            "result": "OK",
            "updated": update_chain,
            "size": size
        })

    def get_app(self):
        app = web.Application()
        app.add_routes([web.post('/add_data', self.add_data),
                        web.get('/add_block', self.add_block),
                        web.get('/get_chain', self.get_chain),
                        web.get('/sync_chain', self.sync_chain),
                        web.get('/register_node', self.register_node),
                        web.get('/', self.help)])
        return app
    
    def start(self):
        app = self.get_app()
        web.run_app(app, host=self.host, port=self.port)