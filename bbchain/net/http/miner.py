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

from bbchain.settings import logger
from aiohttp import web
from bbchain.net.http.base import HttpServerBase

class HttpServerMiner(HttpServerBase):
    def __init__(self, host, port, bc, master_nodes):
        HttpServerBase.__init__(host, port, bc, master_nodes, "MINER")

    def get_help(self):
        return {
            "help": []
        }

    async def add_data(self, request):
        json_resp = await request.json()
        data = json_resp["data"]
        last_hash = json_resp["last_hash"]

        current_last_hash = self.bchain.get_last_hash()
        if last_hash != current_last_hash:
            master_node = self.masters[0]
            blocks = self.client.get_bchain_from_master(master_node, current_last_hash)
            for block in reversed(blocks):
                self.bchain.add_checked_block(block)

        new_block = self.bchain.add_data(data)
		
        return web.json_response({ 
            "result": "OK",
            "block": new_block
        })

    def start(self):
        app = web.Application()
        app.add_routes([web.post('/add_data', self.add_data),
                        web.get('/get_node_type', self.get_node_type),
                        web.get('/get_nodes', self.get_nodes),
                        web.get('/', self.help_node)])

        web.run_app(app, host=self.host, port=self.port)
