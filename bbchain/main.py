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

import argparse
import sys
from bbchain.blockchain import BlockChain

def create_node_id(args):
    return "{0}".format(args.port)

def main():
    parser = argparse.ArgumentParser()

    general_grp = parser.add_argument_group("General Options")
    general_grp.add_argument("--nodes", type=str, nargs='+', help='Master-Node host:port list')
    general_grp.add_argument("--host", type=str, help="Node Hostname", default="localhost")
    general_grp.add_argument("--port", type=int, help="Node Port", default="8000")
    general_grp.add_argument("--verbose", help="Verbose mode", action="store_true")

    master_grp = parser.add_argument_group("Master node Options")
    master_grp.add_argument("--clean", help="Delete & clean all (local) db files", action="store_true")
    master_grp.add_argument("--print", help="Show all the blockchain blocks", action="store_true")
    master_grp.add_argument("--start-master", help="Starts Node as a Master node", action="store_true")

    miner_grp = parser.add_argument_group("Miner node Options")
    miner_grp.add_argument("--start-miner", help="Starts Node as a Miner (validator) node",
                           action="store_true")

    client_grp = parser.add_argument_group("Client Options")
    client_grp.add_argument("--add", help="Adds data to the blockchain. Creating a new Block", type=str)

    args = parser.parse_args()

    # print(args); sys.exit(0)

    node_id = create_node_id(args)

    bc = BlockChain.default(node_id)
    if args.clean:
        bc.clean_db()
        sys.exit(0)
    elif args.print:
        bc.print()
    elif args.add:
        bc.add_data(args.add)
    elif args.start_master:
        from bbchain.settings import Master
        server = Master(args.host, args.port, bc, args.nodes)
        server.start()
    elif args.start_miner:
        from bbchain.settings import Miner
        server = Miner(args.host, args.port, bc, args.nodes)
        server.start()
    else:
        parser.print_help()
