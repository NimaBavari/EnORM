"""Contains :class:`.db_engine.DBEngine`."""

import pyodbc


class DBEngine:
    """Connection adapter for the :class:`.db_session.DBSession` object.

    This provides a thin wrapper around DB driver API.

    :param conn_str:    Database location, along with auth params.

    The class keeps record of the most recent active instance as an inner state.
    """

    active_instance = None

    def __init__(self, conn_str: str) -> None:
        self.conn = pyodbc.connect(conn_str)
        self.cursor = self.conn.cursor()
