"""Contains :class:`.pool.ConnectionPool`."""

from queue import Queue
from threading import Lock
from typing import Optional

import pyodbc


class ConnectionPool:
    """Thread-safe connection pool for managing database connections.

    Uses a FIFO queue to manage connections. Implements lazy initialization of connections.

    :param conn_str:    database location, along with auth params
    :param pool_size:   size of the connection pool.
    """

    def __init__(self, conn_str: str, pool_size: int) -> None:
        self.conn_str = conn_str
        self.pool = Queue(maxsize=pool_size)
        self.lock = Lock()

    def acquire(self, timeout: Optional[float] = None) -> pyodbc.Connection:
        """Acquires a connection from the pool."""
        with self.lock:
            if self.pool.empty():
                return pyodbc.connect(self.conn_str)
        return self.pool.get(timeout=timeout)

    def release(self, conn: pyodbc.Connection) -> None:
        """Releases a connection back to the pool."""
        self.pool.put(conn)

    def close_all(self) -> None:
        """Closes all connections in the pool."""
        while not self.pool.empty():
            conn = self.pool.get()
            conn.close()
