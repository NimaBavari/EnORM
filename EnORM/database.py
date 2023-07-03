from __future__ import annotations

from types import TracebackType
from typing import Any, Dict, Iterator, List, Optional, Type, Union

import pyodbc

from .column import Column, Label
from .model import Model, defined_model_qs
from .query import Query


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
        self.data: Dict[str, List[Any]] = {}
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

    def query(self, *fields: Union[Type, Column, Label]) -> Query:
        return Query(*fields, session=self)

    def add(self, obj: Model) -> None:
        self.queue.append(obj)

    @property
    def _sql(self) -> str:
        """Gets the SQL representation of the current query.

        :return: valid SQL string.
        """
        builder = SQLBuilder(self.data)
        return builder.parse()

    def save(self) -> None:
        self._cursor.execute(self._sql)
        self._conn.commit()
        self.queue = []

    def commit_adds(self) -> None:
        for itm in self:
            self._cursor.execute(itm.sql, *itm.attrs.values())

        self._conn.commit()

        self.queue = []
