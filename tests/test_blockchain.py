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

from bbchain.blockchain import BlockChain
from bbchain.storage import MemoryDB
from bbchain.consensus import SimpleConsensus
from bbchain.settings import logger

class TestBlockchain(unittest.TestCase):
    def default_bc(self):
        mm = MemoryDB()
        cons = SimpleConsensus()
        return BlockChain(mm, cons)

    def test_init(self):
        logger.disabled = True
        bc = self.default_bc()
        self.assertIsNotNone(bc.get_last_hash())