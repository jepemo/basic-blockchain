import time

from bbchain.settings import logger
from multiprocessing import Process

class Supervisor:
    def __init__(self, children={}):
        self.children = {}

    def start():
        self.runtimes = {}
        for name, proc in self.process_list.items():
            p = Process(target=proc.start, args=())
            p.start()
            self.runtimes[name] = p

        sup = Process(target=self.supervise, args=(self.runtimes))
        sup.start()
        sup.join()

    def supervise(self, runtimes):
        while True:
            time.sleep(10)
            # Check processes health

