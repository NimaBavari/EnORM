from typing import Any, Dict, List

import pyodbc


class DBEngine:
    """Docstring here."""

    def __init__(self, conn_str: str) -> None:
        self.conn_str = conn_str

    def connect(self) -> pyodbc.Connection:
        return pyodbc.connect(self.conn_str)


class SQLBuilder:
    """Docstring here."""

    def __init__(self, data: Dict[str, List[Any]]) -> None:
        self.data = data

    def parse(self) -> str:
        return "Parsed value"  # TODO: implement this


class Record:
    """Docstring here."""
