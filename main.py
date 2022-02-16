import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s %(process)s', )
exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      logging.debug("Starting " + self.name)
      logging.debug('sleeping for 5 seconds')
      time.sleep(315)
      logging.debug ("Exiting " + self.name)

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread1.start()

logging.debug('waiting for thread 1')

# here in join thread main is active waiting, heavy performance
# current_thread_wait_for(thread1)
thread1.join() # wait for thread 1 to finish

logging.debug('thread 1 finished')
logging.debug('done')

# loading table
# new_thread -> bring data
# print inside table : "waiting for data ..."
# join (new_thread, 3 seconds)
# print inside table : "slow internet connection ..."

# thread_go_play
# join thread(60 * 60) -- wait for thread to finish
# drive home