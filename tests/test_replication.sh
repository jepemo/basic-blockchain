#!/bin/bash

echo "** DATA TEST **"
echo "> Starting master in port 8000"
bbchain --start-master --port 8000 >/dev/null 2>&1 &
sleep 5

echo "> Starting miner in port 8001"
bbchain --start-miner  --port 8001 --nodes 127.0.0.1:8000 >/dev/null 2>&1 &
sleep 5

echo "> Starting miner in port 8002"
bbchain --start-miner  --port 8002 --nodes 127.0.0.1:8000 >/dev/null 2>&1 &
sleep 5

echo "> Adding some data"
bbchain --port 8003 --nodes 127.0.0.1:8000 --add "Test Data"
sleep 5

echo "> Print"
bbchain --port 8001 --print

killall -9 bbchain

bbchain --port 8000 --clean
bbchain --port 8001 --clean
bbchain --port 8002 --clean
bbchain --port 8003 --clean
