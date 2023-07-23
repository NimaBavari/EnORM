import pyodbc


class DBEngine:
    """Docstring here."""

    active_instance = None

    def __init__(self, conn_str: str) -> None:
        self.conn = pyodbc.connect(conn_str)
        self.cursor = self.conn.cursor()
