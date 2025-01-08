"""Contains abstract and concrete database engine classes, as well as the dialect inferrer class."""

from urllib.parse import urlparse

import pyodbc

from .pool import ConnectionPool


class DialectInferrer:
    """Delegatee class concerning with encapsulation of the sql dialect inferrence functionality.

    :param conn_str:    The database connection string used to infer the SQL dialect.
    """

    def __init__(self, conn_str: str) -> None:
        self.conn_str = conn_str

    @property
    def sql_dialect(self) -> str:
        """Infers the SQL dialect from the connection string."""
        parsed_url = urlparse(self.conn_str)
        if not parsed_url.scheme:
            raise ValueError("Connection string is missing a scheme.")

        dialect = parsed_url.scheme
        if "+" in dialect:
            dialect = dialect.split("+")[0]

        if dialect in ("mssql", "sqlserver"):
            dialect = "sql_server"

        return dialect


class AbstractEngine:
    """Abstract database engine class."""

    active_instance = None


class DBEngine(AbstractEngine):
    """Connection adapter for the :class:`.db_session.DBSession` object.

    Downstream from a thread-safe connection pool. This connection pool uses lazy loading.

    The class keeps record of the most recent active instance as an inner state.

    :param conn_str:    database location, along with auth params
    :param pool_size:   keyword-only. Size of the connection pool.
    """

    def __init__(self, conn_str: str, *, pool_size: int) -> None:
        self.dialect_inferrer = DialectInferrer(conn_str)
        self.dialect = self.dialect_inferrer.sql_dialect
        self.connection_pool = ConnectionPool(conn_str, pool_size)
        self.conn = self.get_connection()
        self.cursor = self.conn.cursor()

    def get_connection(self) -> pyodbc.Connection:
        """Gets a connection from the pool."""
        return self.connection_pool.acquire()

    def release_connection(self, conn: pyodbc.Connection) -> None:
        """Releases a connection back to the pool."""
        self.connection_pool.release(conn)
