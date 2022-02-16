from threading import Semaphore, Thread, Event
import json
import time
import sys
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )

def wait_for_event(e):
    logging.debug('wait_for_event starting')
    event_is_set = e.wait()
    logging.debug('event set: %s', event_is_set)


def wait_for_event_timeout(e, t):
    while not e.is_set():
        logging.debug('wait_for_event_timeout starting')
        event_is_set = e.wait(t)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other things')

if __name__ == '__main__':
    e = Event()
    t1 = Thread(name='blocking',
                          target=wait_for_event,
                          args=(e,))
    t1.start()

    t2 = Thread(name='non-blocking',
                          target=wait_for_event_timeout,
                          args=(e, 5))
    t2.start()

    logging.debug('Waiting before calling Event.set()')
    time.sleep(10)
    e.set()
    logging.debug('Event is set')


sys.exit(0)