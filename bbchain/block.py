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

import time

class Block(object):
    def __init__(self, data, prev_block_hash):
        self.timestamp = time.time()
        self.data = data
        self.prev_block_hash = prev_block_hash
        self.hash = None

    def to_dict(self):
        return {
            "hash": self.hash,
            "prev_block_hash": self.prev_block_hash, #.decode("utf-8"),
            "timestamp": self.timestamp,
            "data": self.data,
        }

    def __str__(self):
        import json
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(d):
        block = Block(
            d["data"],
            d["prev_block_hash"]
        )
        block.timestamp = float(d["timestamp"])
        block.hash = d["hash"]
        return block
