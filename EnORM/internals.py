from __future__ import annotations

from typing import Any, Dict, List

import pyodbc

from .model import Model


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


class Record(tuple, Model):
    """Docstring here."""


class QuerySet:
    """Docstring here."""

    def __init__(self, lst: List[Any]):
        self.lst = lst

    def __len__(self) -> int:
        return len(self.lst)

    def __getitem__(self, key: int) -> Record:
        return self.lst[key]

    def __setitem__(self, key: int, value: Record) -> None:
        self.lst[key] = value

    def __delitem__(self, key: int) -> None:
        del self.lst[key]

    def __getslice__(self, start: int, stop: int) -> QuerySet:
        return QuerySet(self.lst[start:stop])

    def __setslice__(self, start: int, stop: int, sequence: List[Any]) -> None:
        self.lst[start:stop] = sequence

    def __delslice__(self, start: int, stop: int) -> None:
        del self.lst[start:stop]
