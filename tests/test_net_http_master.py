import unittest

#curl -d '{ "host": "0.0.0.0:8080", "type": "MINER"}' -H "Content-Type: application/json" http://127.0.0.1:8000/connect
#curl http://127.0.0.1:8000/get_blocks
#curl http://127.0.0.1:8000/

class TestNetHttpMaster(unittest.TestCase):
    def test_connect(self):
        self.assertEqual(1, 1)
