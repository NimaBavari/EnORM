"""Contains abstract and concrete database engine classes."""

import pyodbc

from .pool import ConnectionPool


class AbstractEngine:
    """Abstract database engine class."""

    active_instance = None


class DBEngine(AbstractEngine):
    """Connection adapter for the :class:`.db_session.DBSession` object.

    This provides a thin wrapper around DB driver API.

    The class keeps record of the most recent active instance as an inner state.

    :param conn_str:    database location, along with auth params
    :param pool_size:   keyword-only. Size of the connection pool.
    """

    def __init__(self, conn_str: str, *, pool_size: int) -> None:
        self.connection_pool = ConnectionPool(conn_str, pool_size)
        self.conn = self.get_connection()
        self.cursor = self.conn.cursor()

    def get_connection(self) -> pyodbc.Connection:
        """Gets a connection from the pool."""
        return self.connection_pool.acquire()

    def release_connection(self, conn: pyodbc.Connection) -> None:
        """Releases a connection back to the pool."""
        self.connection_pool.release(conn)
