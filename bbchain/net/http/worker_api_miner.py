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

class WorkerApiMiner(SenderReceiver):
    def __init__(self, host, port, sync_thread, bchain_thread):
        SenderReceiver.__init__(self)
        self.host = host
        self.port = port
        self.sync_thread = sync_thread
        self.bchain_thread = bchain_thread

    async def help_miner(self, request):
        help = {
            "help": []
        }
        return web.json_response(help)

    async def get_node_type(self, request):
        return web.json_response({'type': "MINER"})

    async def add_data(self, request):
        return web.json_response({})

    def start(self):
        app = web.Application()
        app.add_routes([web.post('/add_data', self.add_data),
                        web.get('/get_node_type', self.get_node_type),
                        web.get('/', self.help_miner)])

        web.run_app(app, host=self.host, port=self.port)
