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


from aiohttp import web
from bbchain.net.network import SenderReceiver
from bbchain.settings import logger

class WorkerApiMaster(SenderReceiver):
    def __init__(self, host, port, sync_thread, bchain_thread):
        SenderReceiver.__init__(self)

        self.host = host
        self.port = port
        self.sync_thread = sync_thread
        self.bchain_thread = bchain_thread

    async def help_master(self, request):
        help = {
            "help": [
                "get_blocks",
            ]
        }
        return web.json_response(help)

    async def connect(self, request):
        info = await request.json()
        node_host = info['host']
        node_type = info['type']
        self.send_command(self.sync_thread, "ADD_NODE", node_host, node_type)
        return web.json_response({'result': "OK"})

    async def get_node_type(self, request):
        return web.json_response({'type': "MASTER"})

    async def get_nodes(self, request):
        self.send_command(self.sync_thread, "NODES")
        sender, result, *args = self.get_command()
        return web.json_response(result)

    async def get_blocks(self, request):
        q = request.rel_url.query
        count = int(q['count']) if 'count' in q else 10
        pointer = q['from_hash'] if 'from_hash' in q else None

        self.send_command(self.bchain_thread, "GET_BLOCKS", count, pointer)
        sender, result, *args = self.get_command()

        return web.json_response({ 'chain': result})

    async def add_data(self, request):
        content = await request.json()
        data = content["data"]
        self.send_command(self.sync_thread, "ADD_DATA_TO_MINER", data)
        return web.json_response({'result': "OK"})

    async def add_block(self, request):
        content = await request.json()
        block = content["block"]

        self.send_command(self.bchain_thread, "ADD_BLOCK", block)
        # Aqui hay que comprobar si el bloque es valido o no antes de insertarlo
        return web.json_response({'result': "OK"})


    def start(self):
        app = web.Application()
        app.add_routes([web.post('/connect', self.connect),
                        web.post('/add_data', self.add_data),
                        web.post('/add_block', self.add_block),
                        web.get('/get_nodes', self.get_nodes),
                        web.get('/get_node_type', self.get_node_type),
                        web.get('/get_blocks', self.get_blocks),
                        web.get('/', self.help_master)])

        web.run_app(app, host=self.host, port=self.port)
