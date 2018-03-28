echo "** DATA TEST **"
echo "> Starting master in port 8000"
bbchain --start-master --port 8000 >/dev/null 2>&1 &
sleep 5

echo "> Starting miner in port 8001"
bbchain --start-miner  --port 8001 --nodes 127.0.0.1:8000 >/dev/null 2>&1 &
sleep 5

echo "> Starting master in port 8002"
bbchain --start-master --port 8002 --nodes 127.0.0.1:8000 >/dev/null 2>&1 &
sleep 5

bbchain --add "Test Data"
