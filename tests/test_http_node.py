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

import unittest
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from bbchain.blockchain import BlockChain
from bbchain.storage import MemoryDB
from bbchain.consensus import SimpleConsensus
from bbchain.settings import logger

# Check:
# https://aiohttp.readthedocs.io/en/v0.22.3/testing.html

class TestHttpNode(AioHTTPTestCase):
    def default_bc(self):
        mm = MemoryDB()
        cons = SimpleConsensus()
        return BlockChain(mm, cons)

    async def get_application(self):
        from bbchain.net.http.node import HttpNode
        Node = HttpNode
        bc = self.default_bc()
        node = Node('localhost', '8080', bc, [])
        return node.get_app()

    @unittest_run_loop
    async def test_help(self):
        logger.disabled = True
        request = await self.client.request("GET", "/")
        assert request.status == 200
        json_res = await request.json()
        assert len(json_res["help"]) > 0