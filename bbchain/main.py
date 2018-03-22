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

import argparse
import sys
from bbchain.blockchain import BlockChain

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", help="Delete & clean all db files", action="store_true")
    parser.add_argument("--print", help="Show all the blockchain blocks", action="store_true")
    parser.add_argument("--add", help="Adds data to the blockchain. Creating a new Block", type=str)
    args = parser.parse_args()
    
    # print(args)
    
    bc = BlockChain.default()
    if args.clean:
        bc.clean_db()
        sys.exit(0)
    elif args.print:
        bc.print()
    elif args.add:
        bc.add_block(args.add)
    else:
        parser.print_help()

