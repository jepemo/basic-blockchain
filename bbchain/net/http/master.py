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

import queue
import sys
import threading
import time
from japronto import Application
from bbchain.net.network import Server, BBProcess, SenderReceiver
from bbchain.settings import logger, client

class BlockchainThread(BBProcess):
    def __init__(self, bc):
        super().__init__("Blockchain")
        self.bchain = bc

    def run(self):
        while True:
            sender, command, *args = self.get_command()
            if command == "EXIT":
                logger.info("Exitting BlockChain Process")
                break
            elif command == "GET_BLOCKS":
                chain = []
                while pointer and count > 0:
                    block = self.bchain.db.get_block(pointer)
                    chain.append(block.to_dict())
                    pointer = block.prev_block_hash
                    count -= 1
                self.send_command(sender, chain)



class SyncThread(BBProcess):
    MAX_TIME_SYNC_NODES = 10

    def __init__(self, hosts, bchain_thread):
        super().__init__("Sync")
        self.masters = []
        self.miners = []
        self.client = client
        self.bchain_thread = bchain_thread
        self.timer_sync_nodes = self.MAX_TIME_SYNC_NODES

    def _decrease_timers(self):
        self.timer_sync_nodes -= 1

    def _sync_nodes(self):
        logger.info("Synchronizing Nodes")
        for m in master:
            ntype = self.client.get_node_type(m)

    def run(self):
        while True:
            if self.command_exists():
                sender, command, *args = self.get_command()
                logger.debug("> Sync Receiced command: " + command)
                if command == "EXIT":
                    logger.info("Exitting Sync Process")
                    break
                elif command == "ADD_NODE":
                    node_host = args[0]
                    node_type = args[1]
                    logger.debug("Adding Node {0} of type {1}".format(node_host, node_type))
                    if node_type == "MASTER" and node_host not in self.masters:
                        self.masters.append(node_host)
                    elif node_type == "MINER" and node_host not in self.miners:
                        self.miners.append(node_host)
                elif command == "NODES":
                    nodes = {
                        'masters': self.masters,
                        'miners': self.miners,
                    }
                    logger.debug("Sending nodes info:", nodes)
                    self.send_command(sender, nodes)

            self._decrease_timers()
            if self.timer_sync_nodes <= 0:
                self._sync_nodes()
                self.timer_sync_nodes = self.MAX_TIME_SYNC_NODES
            time.sleep(1)


class HttpServerMaster(Server, SenderReceiver):
    def __init__(self, host, port, bc, nodes):
        super().__init__(host, port, bc, [], client)
        SenderReceiver.__init__(self)
        self.nodes = nodes

    def help_master(self, request):
        return request.Response(json={
            "help": [
                "get_blocks",
            ]
        })

    def connect(self, request):
        info = request.json
        node_host = info['host']
        node_type = info['type']
        self.send_command(self.sync_thread, "ADD_NODE", node_host, node_type)
        return request.Response(json={'result': "OK"})

    def get_node_type(self, request):
        return request.Response(json={'type': "MASTER"})

    def get_nodes(self, request):
        self.send_command(self.sync_thread, "NODES")
        sender, result, *args = self.get_command()
        request.Response(json=result)

    def get_blocks(self, request):
        count = int(request.query['count']) if 'count' in request.query else 10
        pointer = request.query['from_hash'] if 'from_hash' in request.query else self.bchain.last_hash

        self.send_command(self.sync_thread, "GET_BLOCKS", count, pointer)
        sender, result, *args = self.get_command()

        return request.Response(json={ 'chain': result})

    def start_api(self):
        app = Application()
        app.router.add_route("/connect", self.connect)
        app.router.add_route("/get_nodes", self.get_nodes)
        app.router.add_route('/get_node_type', self.get_node_type)
        app.router.add_route('/get_blocks', self.get_blocks)
        app.router.add_route('/', self.help_master)
        app.run(debug=True, host=self.host, port=self.port)

    def start(self):
        hosts = ["http://" + c for c in self.nodes] if self.nodes else []

        self.bchain_thread = BlockchainThread(self.bchain)
        self.sync_thread = SyncThread(hosts, self.bchain_thread)

        self.sync_thread.start()
        self.bchain_thread.start()

        self.start_api()

        logger.info("Exitting API Process")

        self.send_command(self.bchain_thread, "EXIT")
        self.send_command(self.sync_thread, "EXIT")

        self.sync_thread.join()
        self.bchain_thread.join()
