#curl -d '{ "host": "0.0.0.0:8080", "type": "MINER"}' -H "Content-Type: application/json" http://127.0.0.1:8000/connect
#curl http://127.0.0.1:8000/get_blocks
#curl http://127.0.0.1:8000/

echo "** CONNECTION TEST **"
echo "> Starting master in port 8000"
bbchain --start-master --port 8000 >/dev/null 2>&1 &
sleep 5

echo "> Starting miner in port 8001"
bbchain --start-miner  --port 8001 --nodes 127.0.0.1:8000 >/dev/null 2>&1 &
sleep 5

echo "> Starting master in port 8002"
bbchain --start-master --port 8002 --nodes 127.0.0.1:8000 >/dev/null 2>&1 &
sleep 5

result=$(curl -s http://127.0.0.1:8002/get_nodes)

killall -9 bbchain
sleep 2

bbchain --port 8000 --clean
bbchain --port 8001 --clean
bbchain --port 8002 --clean

read -r -d '' expected << EOM
{"masters": ["http://127.0.0.1:8000", "http://localhost:8002"], "miners": ["http://localhost:8001"]}
EOM
echo "Expected: $expected"
echo "Result:   $result"
