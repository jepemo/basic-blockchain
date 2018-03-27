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

from bbchain.net.network import SenderReceiver
from bbchain.settings import logger
from bbchain.net.http.worker_api_miner import WorkerApiMiner
from bbchain.net.http.worker_bchain import WorkerBlockchain
from bbchain.net.http.worker_sync import WorkerSync


class HttpServerMiner(SenderReceiver):
	def __init__(self, host, port, bc, nodes):
		SenderReceiver.__init__(self)
		self.port = port
		self.host = host
		self.nodes = nodes
		self.bchain = bc

	def start(self):
		self.bchain_worker = WorkerBlockchain(self.bchain)
		self.bchain_worker.start()

		hosts = ["http://" + c for c in self.nodes] if self.nodes else []
		self.sync_worker = WorkerSync(self.bchain_worker, hosts)
		self.sync_worker.start()

		api = WorkerApiMiner(self.host, self.port, self.sync_worker,
						     self.bchain_worker)
		api.start()

		logger.info("Exitting API Miner Process")

		self.send_command(self.bchain_worker, "EXIT")
		self.send_command(self.sync_worker, "EXIT")
		self.bchain_worker.join()
		self.sync_worker.join()
