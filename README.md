# basic-blockchain
Basic cryptocurrency, based on blockchain, implemented in Python

- [Getting started](#getting-started)
  - [Installation](#installation)
  - [Use](#use)
- [Development](#development)
- [Architecture](#architecture)
- [Some readings](#some-readings)

## Getting Started

### Installation
```
pip install bbchain
```

### Use
There are two types of nodes: masters and miners.

#### Masters

Masters have all the blockchain database, sync with other masters to stay update and send data to miners to create blocks.

To start a master node:
```bash
bbchain --start-master
```
But this node is alone. It can be connected to another master:
```bash
bbchain --start-master --nodes ip1:port1,ip2:port2,etc
```

For example, to start in local two master nodes:
```
bbchain --start-master --port 8000 &
bbchain --start-master --port 8001 --nodes 127.0.0.1:8000
```

#### Miners
Miners are connected to master nodes and are waiting data to create blocks. Then, blocks are sent to master nodes.

Miners nodes needs to be connected to a master node.
```bash
bbchain --start-miner --nodes 127.0.0.1:8000
```

#### Adding data to the blockchain.

You can add data to the blockchain.

```
bbchain --nodes 127.0.0.1:8000 --add "Some data"
```

## Development
```bash
git clone https://github.com/jepemo/basic-blockchain.git
cd basic-blockchain
python3 -m venv venv
source venv/bin/activate
pip install -e .

bbchain --help
```

Execute tests:
```
  make test
```

## Architecture

- **bbchain** node:

```
 -----------------------------------
|  ---------------           -----  |           
| | bchain worker | <------ | API | | <---------\
|  ---------------           -----  |           |
|        ^                     |    |           |-> Other bbchain nodes...
|        |                     |    |           |
|  --------------              |    |           |
| | sync worker  | <----------------------------/
|  --------------                   |
 -----------------------------------
```

## Some readings
* [Intro Blockchain Architecture](https://www.pluralsight.com/guides/software-engineering-best-practices/blockchain-architecture)
* [Learn Blockchains by Building One](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46?gi=9fbd0628b089)
* Building Blochain in go:
  * [Part 1: Basic Prototype](https://jeiwan.cc/posts/building-blockchain-in-go-part-1/)
  * [Part 2: Proof-of-Work](https://jeiwan.cc/posts/building-blockchain-in-go-part-2/)
  * [Part 3: Persistence and CLI](https://jeiwan.cc/posts/building-blockchain-in-go-part-3/)
  * [Part 4: Transactions 1](https://jeiwan.cc/posts/building-blockchain-in-go-part-4/)
  * [Part 5: Addresses](https://jeiwan.cc/posts/building-blockchain-in-go-part-5/)
  * [Part 6: Transactions 2](https://jeiwan.cc/posts/building-blockchain-in-go-part-6/)
  * [Part 7: Network](https://jeiwan.cc/posts/building-blockchain-in-go-part-7/)
* [An anonymous proof-of-work blockchain (Implemented in Ruby)](https://github.com/alexdovzhanyn/odyn)
* [Paper review. Blockchains from a distributed computing perspective](http://muratbuffalo.blogspot.com.es/2018/02/blockchains-from-distributed-computing.html)
* [How To Become A Blockchain Developer: Crash Course!](https://blockgeeks.com/guides/blockchain-developer/)
