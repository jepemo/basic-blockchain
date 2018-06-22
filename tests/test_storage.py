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

from bbchain.storage import MemoryDB
from bbchain.block import Block

class TestMemoryDb(unittest.TestCase):
    def create_block(self, data='abcdefghijklmnopqkrsuvwxyz', prev_hash='0000000000000000000000'):
        block = Block(data, prev_hash)
        return block

    def test_add_block(self):
        db = MemoryDB()

        myhash = 'myhash'
        block = self.create_block()
        block.hash = myhash
        
        key = db.add_block(block)

        self.assertIsNotNone(key)

    def test_get_block(self):
        db = MemoryDB()
        
        myhash = 'myhash'
        block = self.create_block()
        block.hash = myhash

        key = db.add_block(block)

        saved_block = db.get_block(myhash)
        self.assertIsNotNone(saved_block)
        # self.assertEqual(saved_block.hash, myhash)

        saved_block = db.get_block(key)
        self.assertIsNotNone(saved_block)
        # self.assertEqual(saved_block.hash, myhash)

    def test_clean_db(self):
        db = MemoryDB()

        myhash = 'myhash'
        block = self.create_block()
        block.hash = myhash
        db.add_block(block)

        self.assertTrue(not db.is_empty())

        db.clean_db()

        self.assertTrue(db.is_empty())

    
    def test_last_hash(self):
        db = MemoryDB()

        myhash = 'myhash'
        block = self.create_block()
        block.hash = myhash

        key = db.add_block(block)
        last_key = db.get_last_hash()

        self.assertEqual(key, last_key)