from ConnectionPoolSingleton import ConnectionPoolSingleton
from MyConnection import MyConnection
from threading import Semaphore, Thread
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )

pool = ConnectionPoolSingleton.get_instance()

conn1 = pool.get_connection()
#logging.debug(conn1)
conn2 = pool.get_connection()
#logging.debug(conn2)

def delay_return(t, conn):
    time.sleep(t)
    pool.return_connection(conn)

def delay_take(t):
    time.sleep(t)
    pool.get_connection()

Thread(name='thread-3', target=delay_take,
                          args=(2,)).start()

Thread(name='thread-1', target=delay_return,
                          args=(5,conn2)).start()

conn3 = pool.get_connection()
#logging.debug(conn3)

Thread(name='thread-2', target=delay_return,
                          args=(3,conn2)).start()
Thread(name='thread-4', target=delay_return,
                          args=(5,MyConnection(20))).start()
conn4 = pool.get_connection()
#logging.debug(conn4)

