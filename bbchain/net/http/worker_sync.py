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
    MAX_TIME_SYNC_NODES = 120
    MAX_TIME_SYNC_CHAIN = 60
    #MAX_TIME_UPTD_CHAIN = 5

    def __init__(self, bc, master_nodes, node_addr, node_type):
        super().__init__("SyncWorker")
        self.bchain_worker = bc
        self.masters = master_nodes
        self.miners = []
        self.client = HttpClient()
        self.node_addr = node_addr
        self.node_type = node_type
        self.timer_sync_nodes = self.MAX_TIME_SYNC_NODES
        self.timer_sync_chain = self.MAX_TIME_SYNC_CHAIN
        #self.timer_uptd_chain = self.MAX_TIME_UPTD_CHAIN
        #self.last_hash = None

    def _decrease_timers(self):
        self.timer_sync_nodes -= 1
        self.timer_sync_chain -= 1
        #self.timer_uptd_chain -= 1

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

    """
    def _update_hash(self):
        self.send_command(self.bchain_worker, "GET_LAST_HASH")
        sender, result, args = self.get_command()
        self.last_hash = result
    """

    def _sync_chain(self):
        logger.info("Synchronizing Chain")
        # TODO

    def _connect(self):
        for m in self.masters:
            logger.info("Connecting to " + m)
            self.client.connect(m, self.node_addr, self.node_type)

    def _add_node(self, node_host, node_type):
        logger.debug("Adding Node {0} of type {1}".format(node_host, node_type))
        if node_type == "MASTER" and node_host not in self.masters:
            self.masters.append(node_host)
        elif node_type == "MINER" and node_host not in self.miners:
            self.miners.append(node_host)

    def _add_data(self, data):
        if not self.miners or len(self.miners) == 0:
            logger.error("This node is not connected to any miner.")
            return

        for m in self.miners:
            self.client.send_data_to_miner(m, data)

    """
    def _check_updated_chain(self):
        if not actual_hash:
            self._update_hash()

        actual_hash = self.last_hash
        self._update_hash()
    """

    def _send_block_master(self, block):
        addr = self.masters[0]
        self.client.send_block_to_master(addr, block)

    def run(self):
        logger.info("sync worker start...")

        # Initial sync
        self._connect()
        self._sync_nodes()
        self._sync_chain()
        #self._update_hash()

        while True:
            if self.command_exists():
                sender, command, args = self.get_command()
                logger.debug("Processing: {0}({1})".format(command, args))
                if command == "EXIT":
                    logger.info("Exitting Sync Process")
                    break
                elif command == "ADD_NODE":
                    node_host = args[0]
                    node_type = args[1]
                    self._add_node(node_host, node_type)
                elif command == "NODES":
                    nodes = {
                        'masters': self.masters,
                        'miners': self.miners,
                    }
                    logger.debug("Sending nodes info:", nodes)
                    self.send_command(sender, nodes)
                elif command == "ADD_DATA":
                    data = args[0]
                    self._add_data(data)
                    xx, block, zz = self.get_command()
                    self._send_block_master(block)
            else:
                self._decrease_timers()
                if self.timer_sync_nodes <= 0:
                    self._sync_nodes()
                    self.timer_sync_nodes = self.MAX_TIME_SYNC_NODES
                if self.timer_sync_chain <= 0:
                    self._sync_chain()
                    self.timer_sync_chain = self.MAX_TIME_SYNC_CHAIN
                #if self.timer_uptd_chain <= 0
                #    self._check_updated_chain()
                #    self.timer_uptd_chain = self.MAX_TIME_UPTD_CHAIN
            time.sleep(1)
