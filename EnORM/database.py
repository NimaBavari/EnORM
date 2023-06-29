from __future__ import annotations

from types import TracebackType
from typing import Any, Iterator, List, Optional, Type, Union

import pyodbc

from .column import Column, Label
from .model import Model
from .query import Query


class DBEngine:
    """Docstring here."""

    def __init__(self, conn_str: str) -> None:
        self.conn_str = conn_str

    def connect(self) -> pyodbc.Connection:
        return pyodbc.connect(self.conn_str)


class DBSession:
    """Docstring here."""

    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> DBSession:
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, conn_str: str) -> None:
        self.engine = DBEngine(conn_str)
        self._conn = self.engine.connect()
        self._cursor = self._conn.cursor()
        self.queue: List[Model] = []

    def __enter__(self) -> Optional[DBSession]:
        return self._instance

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        if self._conn:
            try:
                self.commit()
            except exc_type:
                self._conn.rollback()
                raise
            finally:
                self._cursor.close()
                self._conn.close()
                self._instance = None

    def __iter__(self) -> Iterator[Model]:
        yield from self.queue

    def query(self, *fields: Union[Type, Column, Label]) -> Query:
        return Query(*fields, session=self)

    def add(self, obj: Model) -> None:
        self.queue.append(obj)

    def save(self) -> None:
        # TODO: Get emission of `UPDATE` and `DELETE` from the query. Hooks?
        pass

    def commit(self) -> None:
        for itm in self:
            self._cursor.execute(itm.sql, *itm.attrs.values())

        self._conn.commit()
