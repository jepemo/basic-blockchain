import sys
import time

from bbchain.settings import logger
from multiprocessing import Process

class Supervisor:
    def __init__(self, children={}):
        self.children = children

    def start(self):
        self.runtimes = {}
        for name, proc in self.children.items():
            print(f"Starting process {name}")
            p = Process(target=proc.start, args=())
            logger.info(f"Starting process {name}")
            p.start()
            self.runtimes[name] = p.pid

        logger.info("Starting supervisor")
        sup = Process(target=self.supervise, args=(self.runtimes))
        sup.start()
        sup.join()

    def supervise(self, runtimes={}):
        while True:
            time.sleep(10)
            sys.exit(0)
            # Check processes health

