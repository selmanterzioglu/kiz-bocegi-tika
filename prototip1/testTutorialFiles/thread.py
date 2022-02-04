from concurrent.futures import thread
import logging
from os import truncate 
import threading
import time
import concurrent.futures

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(3)
    logging.info("thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO)
    

    # thread = list()
    # for index in range(3):
    #     logging.info("main: create and start thread %d", index)
    #     x = threading.Thread(target=thread_function, args=(index, ), daemon=True)
    #     thread.append(x)
    #     x.start()
    
    # for index,  thread in enumerate(thread):
    #     logging.info("main: before joining thread %d", index)
    #     thread.join()
    #     logging.info("main: thread %d done",  index)


    # logging.info("main: before creating thread")

    # x = threading.Thread(target = thread_function, args=(1,), daemon=True)

    # logging.info("main: before running thread")
    # x.start()
    # logging.info("wait for the thread to finish")
    # x.join()
    # logging.info("main: all done")



    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, range(3))
        
    

        

    

