"""Contains :class:`.db_session.DBSession`."""

from __future__ import annotations

from types import TracebackType
from typing import Any, Iterator, List, Optional, Type, Union

import pyodbc

from .column import BaseColumn
from .db_engine import AbstractEngine
from .model import Model
from .query import Query


class TransactionManager:
    """A transaction manager class.

    :param engine:  DB engine that the transaction manager uses.

    Used within repository pattern in :class:`.db_session.DBSession`. to manage transactions.
    """

    def __init__(self, engine: AbstractEngine) -> None:
        self.engine = engine

    def commit(self) -> None:
        """Commits the current transaction."""
        self.engine.conn.commit()

    def rollback(self) -> None:
        """Rolls back the current transaction."""
        self.engine.conn.rollback()

    def close(self) -> None:
        """Closes the connection."""
        self.engine.cursor.close()
        self.engine.conn.close()


class PersistenceManager:
    """A persistance manager class.

    :param engine:  DB engine that the persistence manager uses.

    Used within repository pattern in :class:`.db_session.DBSession`. to manage persistence.
    """

    def __init__(self, engine: AbstractEngine) -> None:
        self.engine = engine
        self.queue: List[Model] = []

    def add(self, obj: Model) -> None:
        """Adds an object to the queue for persistence."""
        self.queue.append(obj)

    def auto_commit_adds(self) -> None:
        """Persists all added objects."""
        for itm in self.queue:
            self.engine.cursor.execute(itm.sql, *itm.attrs.values())

        self.engine.conn.commit()

        self.queue = []


class QueryExecutor:
    """A query executor class.

    :param engine:  DB engine that the query executor uses.

    Used within repository pattern in :class:`.db_session.DBSession`. to execute queries.
    """

    def __init__(self, engine: AbstractEngine) -> None:
        self.engine = engine
        self.accumulator: List[Query] = []

    def query(self, *fields: Union[Type, BaseColumn]) -> Query:
        """Starts a query and returns the query object."""
        query = Query(*fields)
        self.accumulator.append(query)
        return query

    def execute_queries(self) -> None:
        """Executes accumulated queries."""
        for query in self.accumulator:
            self.engine.cursor.execute(query._sql)

        self.engine.conn.commit()

        self.accumulator = []


class DBSession:
    """A singleton DB session class.

    This class implements a singleton DB session to be used to access the database.

    :param engine:  DB engine that the session uses.

    Implements a context manager for a more secure session. The following is an idiomatic usage::

        eng = DBEngine("postgresql://user:secret@localhost:5432/my_db")
        with DBSession(eng) as session:
            pass  # do something with session
    """

    _instance: Optional[DBSession] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> DBSession:
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, engine: AbstractEngine) -> None:
        self.engine = engine
        AbstractEngine.active_instance = self.engine

        self.transaction_manager = TransactionManager(self.engine)
        self.persistence_manager = PersistenceManager(self.engine)
        self.query_executor = QueryExecutor(self.engine)

        try:
            for sql in Model.model_definition_sqls:
                self.engine.cursor.execute(sql)
        except pyodbc.DatabaseError:
            raise
        finally:
            Model.model_definition_sqls = []

        self.transaction_manager.commit()

    def __enter__(self) -> DBSession:
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        if not self.engine.conn:
            return

        try:
            self.persistence_manager.auto_commit_adds()
        except exc_type:
            self.transaction_manager.rollback()
            raise
        finally:
            self.transaction_manager.close()
            DBSession._instance = None

    def __iter__(self) -> Iterator[Model]:
        yield from self.persistence_manager.queue

    def query(self, *fields: Union[Type, BaseColumn]) -> Query:
        """Starts a query and returns the query object."""
        return self.query_executor.query(*fields)

    def add(self, obj: Model) -> None:
        """Adds a new record to the DB session."""
        self.persistence_manager.add(obj)

    def save(self) -> None:
        """Persists all started queries."""
        self.query_executor.execute_queries()
