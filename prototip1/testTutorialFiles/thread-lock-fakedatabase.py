import threading
import logging
import time


class FakeDatabase:

    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()


    def locked_update(self, name):
        logging.info("thread %s: starting update", name)
        logging.debug("thread: %s about to lock",  name)
        with self._lock:
            logging.debug("thread %s  has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("thread: %s about to release lock",  name)

        logging.debug("thread %s after felease ",  name)
        logging.info("thread %s: finishing update", name)
        