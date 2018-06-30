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

import coloredlogs, logging

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')

#from bbchain.net.http.master import HttpServerMaster
#Master = HttpServerMaster

#from bbchain.net.http.miner import HttpServerMiner
#Miner = HttpServerMiner

from bbchain.net.http.node import HttpNode
Node = HttpNode

from bbchain.net.http.client import HttpClient
Client = HttpClient
