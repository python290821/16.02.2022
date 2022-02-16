from threading import Lock, Semaphore, Thread, Event
import time
from MyConnection import *
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )

class ConnectionPoolSingleton(object):
    _instance = None
    _lock = Lock()
    _lock_pool = Lock()
    _max_connections = 2

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        with cls._lock:
            if cls._instance is None: #t1 + t2
                cls._instance = cls.__new__(cls)
                cls._instance.connections = [MyConnection(i + 1) for i in range(cls._max_connections)]
                cls._instance.free_conn_event = Event()
                cls._instance.free_conn_event.set()
            return cls._instance

    def get_free_count(self):
        return len(self.connections)

    def get_max_possible_connections(self):
        return ConnectionPoolSingleton._max_connections

    def get_connection(self):
        # will return a connection and remove it from the list
        # return self.connections ...
        # lock
        logging.debug('try to get connection')
        while True:

            if len(self.connections) == 0:
                logging.debug('no more connection, wait ...')
                self.free_conn_event.wait()
                logging.debug('finished waiting')

            with self._lock_pool:
                if len(self.connections) > 0:
                    conn = self.connections.pop(0)
                    logging.debug(f'taking connection {conn.number}')
                    if len(self.connections) == 0:
                        logging.debug('closing the gate - because took last connection')
                        self._instance.free_conn_event.clear();
                    return conn
                else:
                    # safer
                    if self._instance.free_conn_event.is_set:
                        logging.debug('closing the gate for backup')
                        self._instance.free_conn_event.clear();

    def return_connection(self, conn):
        # will take the connection and add it to the list
        # self.connections --> append
        # lock
        # tt
        with self._lock_pool:
            self.connections.append(conn) # list python is thread safe
            self._instance.free_conn_event.set()
            logging.debug(f'returning connection {conn.number}')
