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

    def test_add_data(self):
        logger.disabled = True
        bc = self.default_bc()

        for ind in range(0, 5):
            data = "data{0}".format(ind)
            bc.add_data(data)
            bc.add_block()
        
        print("\nDATOS:")
        # for ind in reversed(range(0, 5)):
        r = list(range(0, 5))
        for ind in r:
            i = list(reversed(r))[ind]
            data = "data{0}".format(i)
            # print(ind, i)
            # print(bc.current_data)
            # print(bc.current_data[ind].strip(), data.strip())
            # print("-------")
            self.assertTrue(bc.current_data[ind] == data)

    def test_add_block(self):
        logger.disabled = True
        bc = self.default_bc()

        for ind in range(0, 5):
            data = "data{0}".format(ind)
            bc.add_data(data)

        block = bc.add_block()
        self.assertIsNotNone(block.hash)

    def test_is_block_valid(self):
        logger.disabled = True
        bc = self.default_bc()

        for ind in range(0, 5):
            data = "data{0}".format(ind)
            bc.add_data(data)

        block = bc.add_block()

        self.assertTrue(bc.is_block_valid(block))

        block.hash = '123456'
        self.assertFalse(bc.is_block_valid(block))