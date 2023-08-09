"""Contains abstract and concrete database engine classes."""

import pyodbc


class AbstractEngine:
    """Abstract database engine class."""

    active_instance = None


class DBEngine(AbstractEngine):
    """Connection adapter for the :class:`.db_session.DBSession` object.

    This provides a thin wrapper around DB driver API.

    :param conn_str:    database location, along with auth params.

    The class keeps record of the most recent active instance as an inner state.
    """

    def __init__(self, conn_str: str) -> None:
        self.conn = pyodbc.connect(conn_str)
        self.cursor = self.conn.cursor()
