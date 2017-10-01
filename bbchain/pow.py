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

import array
import hashlib
import struct
import sys

def dummy_pow():
	pass

def num_to_bytes(num):
	return bytes(array.array('f', [num]))

def bytes_to_num (bts):
	return struct.unpack("<L", bts)[0]

class ProofOfWork(object):
	def __init__(self, block):
		self.target_bits = 24
		self.block = block
		self.target = 1 << (256 - self.target_bits)

	def prepare_data(self, nonce):
		return b''.join ([
			self.block.prev_block_hash,
			bytes(self.block.data.encode("utf8")),
			num_to_bytes(self.block.timestamp),
			num_to_bytes(self.target_bits),
			num_to_bytes(nonce)
		])

	def run(self):
		nonce = 0
		bhash = None

		print ("Mining the block containing {0}".format(self.block.data))
		while nonce < sys.maxsize:
			data = self.prepare_data(nonce)
			print(data)
			bhash = hashlib.sha256(data).digest()
			print(bhash)

			if bytes_to_num(bhash) < int(self.target):
				break
			else:
				nonce += 1

		return nonce, bhash
