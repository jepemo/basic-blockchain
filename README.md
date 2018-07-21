# basic-blockchain
Basic cryptocurrency, based on blockchain, implemented in Python.

- [basic-blockchain](#basic-blockchain)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Use (default web implementation)](#use-default-web-implementation)
  - [Development](#development)
  - [Roadmap](#roadmap)
  - [License](#license)

## Getting Started

### Installation
```
pip install bbchain
```

### Use (default web implementation)

```bash
# Start (default port 8000)
bbchain --start

# Start with selected host/port
bbchain --start --host 127.0.0.1 --port 8002

# Select other nodes to connect
bbchain --start --nodes ip1:port1,ip2:port2

# Add data to the blockchain
bbchain --add "data to storage" --nodes ip1:port1

# Maintenance
## Clean local storage
bbchain --clean
## Show local data
bbchain --print
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
  python3 setup.py test
```


[Some Blockchain implementation readings](docs/readings.md)

## Roadmap
- More tests
- Implement real consensus algorithms
- Improve default http implementation (better sync, etc.)
- Some examples: cryptocurrency, etc.
- Allow to save non-textual data

## License

[GNU GPLv3](LICENSE)

Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights. 
