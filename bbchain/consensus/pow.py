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
import struct
import sys
from bbchain.consensus.consensus import Consensus
from bbchain.utils import num_to_bytes

class ProofOfWork(Consensus):
	def __init__(self):
		self.target_bits = 24
		self.target = 1 << (256 - self.target_bits)

	def _prepare_data(self, block, nonce):
		return b''.join ([
			block.prev_block_hash,
			bytes(block.data.encode("utf8")),
			num_to_bytes(block.timestamp),
			num_to_bytes(self.target_bits),
			num_to_bytes(nonce)
		])

	def calculate_hash(self, block):
		nonce = 0
		bhash = None

		print ("Mining the block containing {0}".format(block.data))
		while nonce < sys.maxsize:
			data = self._prepare_data(block, nonce)
			bhash = hashlib.sha256(data).hexdigest()
			if self.is_valid(bhash):
				break
			else:
				nonce += 1

		return nonce, bytearray.fromhex(bhash)

	def is_valid(self, block_hash):
		return block_hash[-4:] == "0000"
