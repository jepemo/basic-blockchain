# -*- coding: utf-8 -*-
# bbchain - Basic cryptocurrency, based on blockchain, implemented in Python
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

import hashlib
import time

class Block(object):
    def __init__(self, data, prev_block_hash):
        self.timestamp = time.time()
        self.data = data
        self.prev_block_hash = prev_block_hash
        self.hash = self.create_hash()

    def create_hash(self):
        concat = ''.join([str(self.timestamp), str(self.prev_block_hash), str(self.data)])
        return hashlib.sha256(concat.encode('utf8')).digest()
