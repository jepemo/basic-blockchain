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
from bbchain.block import Block
from bbchain.storage import create_db
from bbchain.consensus import create_consensus
from bbchain.settings import logger

class BlockChain(object):
	def __init__(self, db, consensus):
		self.db = db
		self.consensus = consensus

		if self.db.is_empty():
			genesis = self.create_genesis_block()
			self.db.add_block(genesis)

		self.last_hash = self.db.get_last_hash()

	def get_last_hash(self):
		return self.db.get_last_hash()

	def add_data(self, data):
		return self.add_block(data)

	def add_block(self, data):
		new_block = Block(data, self.get_last_hash())
		new_block.hash = self.consensus.calculate_hash(new_block)

		self.add_checked_block(new_block)

		return new_block

	def add_checked_block(self, new_block):
		self.db.add_block(new_block)
		lhash = self.db.get_last_hash()
		self.last_hash = lhash
		#print("\n{}\n{}\n".format(new_block.hash, self.last_hash))
		assert new_block.hash == self.last_hash

		# Update last block
		#last_block = self.db.get_block(new_block.prev_block_hash)
		#last_block.next_block_hash = lhash
		#self.db.add_block(last_block)

	def create_genesis_block(self):
		logger.info("Creating genesis block")
		new_block = Block("Genesis Block", "")
		new_block.hash = self.consensus.calculate_hash(new_block)
		return new_block

	def is_block_valid(self, block):
		return self.consensus.is_valid(block.hash)

	def clean_db(self):
		self.db.clean_db()

	def print(self):
		pointer = self.last_hash
		while pointer:
			block = self.db.get_block(pointer)
			print ("Prev. hash:", block.prev_block_hash)
			print ("Data:", block.data)
			print ("Hash:", block.hash)
			print ("Valid:", self.is_block_valid(block))
			print ("")
			pointer = block.prev_block_hash

	@staticmethod
	def default(node_id):
		return BlockChain(create_db(node_id), create_consensus())
