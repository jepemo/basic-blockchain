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

class WorkerBlockchain(BBProcess):
    def __init__(self, bc):
        super().__init__("Blockchain")
        self.bchain = bc

    def _create_block(self, data):
        return self.bchain.add_data(data)

    def run(self):
        logger.info("bbchain worker start...")
        while True:
            if self.command_exists():
                sender, command, args = self.get_command()
                logger.debug("Processing: {0}({1})".format(command, args))
                if command == "EXIT":
                    logger.info("Exitting BlockChain Process")
                    break
                elif command == "GET_BLOCKS":
                    count = args[0]
                    pointer = args[1] if args[1] else self.bchain.last_hash
                    chain = []
                    while pointer and count > 0:
                        block = self.bchain.db.get_block(pointer)
                        chain.append(block.to_dict())
                        pointer = block.prev_block_hash
                        count -= 1
                    self.send_command(sender, chain)
                elif command == "CREATE_BLOCK":
                    data = args[0]
                    new_block = self._create_block(data)
                    self.send_command(sender, new_block)
                elif command == "ADD_BLOCK":
                    block = args[0]
                    self.bchain.add_checked_block(block)
                    # Hay que devolver si el bloque es valido o no
