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

from bbchain.block import Block

class TestBlock(unittest.TestCase):
    def test_block_todict(self):
        data = '1234567890'
        prev = '0000000000'
        h = '111111111'
        block = Block(data, prev)
        block.hash = h

        bdict = block.to_dict()
        self.assertEqual(bdict['hash'], h)
        self.assertEqual(bdict['prev_block_hash'], prev)
        self.assertIsNotNone(bdict['timestamp'])
        self.assertEqual(bdict['data'], data)


    def test_block_fromdict(self):
        data = '1234567890'
        prev = '0000000000'
        h = '111111111'
        t = '1234567890'

        dblock = {
            'hash': h,
            'prev_block_hash': prev,
            'timestamp': t,
            'data': data,
        }

        block = Block.from_dict(dblock)

        self.assertEqual(block.hash, h)
        self.assertEqual(block.prev_block_hash, prev)
        self.assertTrue(isinstance(block.timestamp, float))
        self.assertEqual(block.data, data)