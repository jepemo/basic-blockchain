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

class Transaction(object):
	def __init__(self, to, data):
		self.tx_inputs = []
		self.tx_outputs = []

		if data == "":
			data = "Reward to '{0}'".format(to)

		txin := TXInput{[]byte{}, -1, data}
		txout := TXOutput{subsidy, to}
		tx := Transaction{nil, []TXInput{txin}, []TXOutput{txout}}
		tx.SetID()


class TxOutput(object):
	def __init__(self):
		self.value = None
		self.script_pub_key = None


class TxInput(object):
	def __init__(self):
		self.tx_id = None
		self.vout = None
		self.script_sig = None
