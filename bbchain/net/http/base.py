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
from aiohttp import web

class HttpServerBase:
    def __init__(self, host, port, bc, master_nodes, node_type):
        self.host = host
        self.port = port
        self.bchain = bc
        self.client = HttpClient()
        self.master_nodes = master_nodes

        self.masters = master_nodes
        self.miners = []
        self.node_type = node_type

    def get_help(self):
        return {}

    async def get_nodes(self, request):
        return web.json_response({
            'masters': self.masters,
            'miners': self.miners,
        })

    async def get_node_type(self, request):
        return web.json_response({'type': self.node_type})

    async def help_node(self, request):
        return web.json_response(self.get_help())