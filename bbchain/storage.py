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

import binascii
import os
import tempfile

class DB(object):
    def add_block(self, _block):
        raise Exception("Not Implemented")
    def get_block(self, _hash):
        raise Exception("Not Implemented")
    def clean_db(self):
        raise Exception("Not Implemented")
    def get_last_hash(self):
        raise Exception("Not Implemented")
    def is_empty(self):
        raise Exception("Not Implemented")

class MemoryDB(DB):
    def __init__(self):
        self.db = {}
        self.last_hash_key = "l"

    def _block_key(self, _hash):
        assert _hash is not None

        if _hash.startswith("b"):
            return _hash
        else:
            return "b" + _hash

    def add_block(self, _block):
        key = self._block_key(_block.hash)
        _block.hash = key
        self.db[key] = _block
        self.db[self.last_hash_key] = key
        return key

    def get_block(self, _hash):
        key = self._block_key(_hash)
        return self.db[key]

    def clean_db(self):
        self.db = []

    def get_last_hash(self):
        key = self.last_hash_key
        return self.db[key] if key in self.db else None

    def is_empty(self):
        return len(self.db) == 0


class ShelveDB(DB):
    shelve = None
    def __init__(self, _node_id, _module, _dbpath):
        self.shelve = _module
        self.blocks_path = os.path.join(_dbpath, "blocks_" + _node_id)
        self.chainstate_path = os.path.join(_dbpath, "chainstate_" + _node_id)
        self.last_hash_key = "l"

    def _block_key(self, _hash):
        if _hash.startswith("b"):
            return _hash
        else:
            return "b" + _hash

    def add_block(self, _block):
        key = self._block_key(_block.hash)
        with self.shelve.open(self.blocks_path) as db:
            db[key] = _block
            db[self.last_hash_key] = key

    def get_block(self, _hash):
        block = None
        key = self._block_key(_hash)
        with self.shelve.open(self.blocks_path) as db:
            block = db[key]
        return block

    def clean_db(self):
        if os.path.exists(self.blocks_path):
            os.remove(self.blocks_path)
        if os.path.exists(self.chainstate_path):
            os.remove(self.chainstate_path)

    def get_last_hash(self):
        last_hash = None
        with self.shelve.open(self.blocks_path) as db:
            last_hash = db[self.last_hash_key]
        return last_hash

    def is_empty(self):
        empty = True
        with self.shelve.open(self.blocks_path) as db:
            # empty = self.last_hash_key in db
            empty = (len(list(db.keys())) == 0)
        return empty


def create_db(node_id, engine="shelve", dbpath=tempfile.gettempdir()):
    if engine == "shelve":
        import shelve
        return ShelveDB(node_id, shelve, dbpath)
