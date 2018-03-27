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
from bbchain.net.network import BBProcess
from bbchain.settings import logger
from bbchain.net.http.client import HttpClient


class WorkerSync(BBProcess):
    MAX_TIME_SYNC_NODES = 100

    def __init__(self, bc, nodes):
        super().__init__("SyncWorker")
        self.masters = []
        self.miners = []
        self.client = HttpClient()
        self.nodes = nodes
        self.timer_sync_nodes = self.MAX_TIME_SYNC_NODES

    def _decrease_timers(self):
        self.timer_sync_nodes -= 1

    def _sync_nodes(self):
        logger.info("Synchronizing Nodes")
        time.sleep(2)
        masters_add = []
        miners_add = []
        for m in self.masters:
            masters, miners = self.client.get_nodes(m)
            masters_add.extend(masters)
            miners_add.extend(miners)

        self.masters.extend(masters_add)
        self.miners.extend(miners_add)
        self.masters = list(set(self.masters))
        self.miners = list(set(self.miners))

    def run(self):
        logger.info("sync worker start...")

        # Initial sync
        self._sync_nodes()

        while True:
            if self.command_exists():
                sender, command, args = self.get_command()
                logger.debug("Processing: {0}({1})".format(command, args))
                if command == "EXIT":
                    logger.info("Exitting Sync Process")
                    break
            else:
                self._decrease_timers()
                if self.timer_sync_nodes <= 0:
                    self._sync_nodes()
                    self.timer_sync_nodes = self.MAX_TIME_SYNC_NODES
                time.sleep(1)
