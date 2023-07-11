from __future__ import annotations

from types import TracebackType
from typing import Any, Iterator, List, Optional, Type, Union

import pyodbc

from .column import BaseColumn, Label
from .model import Model, defined_model_qs
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
        self.accumulator: List[Query] = []
        for query in defined_model_qs:
            self._cursor.execute(query)
        self._conn.commit()

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
                self.commit_adds()
            except exc_type:
                self._conn.rollback()
                raise
            finally:
                self._cursor.close()
                self._conn.close()
                self._instance = None

    def __iter__(self) -> Iterator[Model]:
        yield from self.queue

    def query(self, *fields: Union[Type, BaseColumn, Label]) -> Query:
        q = Query(*fields, session=self)
        self.accumulator.append(q)
        return q

    def add(self, obj: Model) -> None:
        self.queue.append(obj)

    def save(self) -> None:
        for q in self.accumulator:
            self._cursor.execute(q._sql)

        self._conn.commit()

        self.accumulator = []

    def commit_adds(self) -> None:
        for itm in self:
            self._cursor.execute(itm.sql, *itm.attrs.values())

        self._conn.commit()

        self.queue = []
