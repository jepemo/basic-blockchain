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

import hashlib
from bbchain.utils import num_to_bytes

class Consensus(object):
	def calculate_hash(self, block):
		raise Exception("Not implemented")
	def is_valid(self, block_hash):
		raise Exception("Not implemented")

class SimpleConsensus(object):
	def calculate_hash(self, block):
		datablock = datablock = block.data
		if (isinstance(block.data, list)):
			datablock = ''.join(block.data)

		data = b''.join ([
			bytes(block.prev_block_hash.encode("utf8")),
			bytes(datablock.encode("utf8")),
			num_to_bytes(float(block.timestamp))
		])
		return hashlib.sha256(data).hexdigest()

	def is_valid(self, block_hash):
		return True
