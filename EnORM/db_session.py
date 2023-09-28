"""Contains :class:`.db_session.DBSession`."""

from __future__ import annotations

from types import TracebackType
from typing import Any, Iterator, List, Optional, Type, Union

import pyodbc

from .column import BaseColumn, Label
from .db_engine import AbstractEngine
from .model import Model
from .query import Query


class DBSession:
    """A singleton DB session class.

    This class implements a singleton DB session to be used to access the database.

    :param engine:  DB engine that the session uses.

    Implements a context manager for a more secure session. The following is an idiomatic usage::

        eng = DBEngine("postgresql://user:secret@localhost:5432/my_db")
        with DBSession(eng) as session:
            pass  # do something with session
    """

    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> DBSession:
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, engine: AbstractEngine) -> None:
        self.engine = engine
        AbstractEngine.active_instance = self.engine
        self.queue: List[Model] = []
        self.accumulator: List[Query] = []

        try:
            for sql in Model.model_definition_sqls:
                self.engine.cursor.execute(sql)
        except pyodbc.DatabaseError:
            raise
        finally:
            Model.model_definition_sqls = []

        self.engine.conn.commit()

    def __enter__(self) -> Optional[DBSession]:
        return self._instance

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        if self.engine.conn:
            try:
                self.commit_adds()
            except exc_type:
                self.engine.conn.rollback()
                raise
            finally:
                self.engine.cursor.close()
                self.engine.conn.close()
                self._instance = None

    def __iter__(self) -> Iterator[Model]:
        yield from self.queue

    def query(self, *fields: Union[Type, BaseColumn, Label]) -> Query:
        """Starts a query and returns the query object."""
        q = Query(*fields)
        self.accumulator.append(q)
        return q

    def add(self, obj: Model) -> None:
        """Adds a new record to the DB session."""
        self.queue.append(obj)

    def save(self) -> None:
        """Persists all started queries."""
        for q in self.accumulator:
            self.engine.cursor.execute(q._sql)

        self.engine.conn.commit()

        self.accumulator = []

    def commit_adds(self) -> None:
        """Persists all added records on the DB session."""
        for itm in self:
            self.engine.cursor.execute(itm.sql, *itm.attrs.values())

        self.engine.conn.commit()

        self.queue = []
