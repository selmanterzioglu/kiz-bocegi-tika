import logging
import time
import concurrent.futures

class FakeDatabase:

    def __init__(self):
        self.value = 0

    def update(self,  name):
        logging.info("thread: %s:  starting update", name)
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        logging.info("thread %s: finishing update", name)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level = logging.INFO,
                        datefmt="%H:%M:%S")

    database = FakeDatabase()
    logging.info("testing update. starting value is %d", database.value)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers = 2) as executor:
        for  index in range(2):
            executor.submit(database.update, index)
        
    
    logging.info("testing update. ending value is %d", database.value)

