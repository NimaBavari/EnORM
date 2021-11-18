"""Module docstring here."""

from __future__ import annotations

from types import TracebackType
from typing import Any, Dict, Iterator, List, Optional, Tuple, Type, Union

from .column import Column, Label
from .internals import DBEngine, SQLBuilder
from .model import Model


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
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
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

    def save(self, obj: Model) -> None:
        self.queue.append(obj)

    def commit(self) -> None:
        for itm in self:
            self._cursor.execute(itm.sql, *itm.attrs.values())
        self._conn.commit()


class Query:
    """Docstring here."""

    def __init__(self, *entities: Union[Type, Column, Label], session: DBSession) -> None:
        # NOTE: When `all`, `one`, etc. methods (the final methods) are
        # implemented, we need to convert the list of tuples into the list of
        # `Record` objects.
        # NOTE: In future, `expr` will be an actual expression, rather than
        # strings, in `having` method and for each `expr` in `filter` method.
        self.entities = entities
        self.session = session
        self.data: Dict[str, List[Any]] = {}
        if not self.entities:
            raise ValueError("No fields specified for querying.")

        if sum(isinstance(item, type) for item in self.entities) > 1:
            raise ValueError("More than one model specified in the query.")

        for item in self.entities:
            # TODO: Implement functions within query
            if isinstance(item, type):
                self.mapped_class = item
                self._add_to_data("select", "*")
                self._add_to_data("from", item.get_table_name())
            elif isinstance(item, Column):
                try:
                    self._add_to_data(
                        "select",
                        next(k for k, v in item.model.__dict__.items() if v is item),
                    )
                except (AttributeError, StopIteration):
                    raise ValueError("Column name not found.")
                self._add_to_data("from", item.model.get_table_name())
            elif isinstance(item, Label):
                denotee: Union[Type, Column] = item.denotee
                if isinstance(denotee, type):
                    self._add_to_data("select", "*")
                    self._add_to_data("from", denotee.get_table_name())
                    self._add_to_data("from_as", item.text)
                elif isinstance(denotee, Column):
                    try:
                        self._add_to_data(
                            "select",
                            next(k for k, v in denotee.model.__dict__.items() if v is item),
                        )
                    except (AttributeError, StopIteration):
                        raise ValueError("Column name not found.")
                    self._add_to_data("from", denotee.model.get_table_name())
                    self._add_to_data("select_as", item.text)
            else:
                raise TypeError("Wrong query format.")

    def _add_to_data(self, key: str, val: str) -> None:
        self.data[key] = [*self.data.get(key, []), val]

    @property
    def _sql(self) -> str:
        builder = SQLBuilder(self.data)
        return builder.parse()

    @staticmethod
    def parse(expression: str) -> Tuple[str, str, str, str]:
        # TODO: Implement!
        if not hasattr(eval(mapped_class), field_name):
            raise AttributeError("%s does not have field %s" % (mapped_class, field_name))
        return mapped_class, field_name, operator, value

    def filter(self, *exprs: str) -> Query:
        for expr in exprs:
            self._add_to_data("where", "'%s'.'%s' %s %s" % self.parse(expr))
        return self

    def filter_by(self, **kwcrts: Any) -> Query:
        criteria = ["%s.%s == %s" % (self.mapped_class.__name__, key, val) for key, val in kwcrts.items()]
        return self.filter(*criteria)

    def join(self, model_cls: Type) -> Query:
        # TODO: Implement. Note that this is very complicated.
        return self

    def having(self, expr: str) -> Query:
        self._add_to_data("having", "'%s'.'%s' %s %s" % self.parse(expr))
        return self

    def group_by(self, *columns: Optional[Column]) -> Query:
        cleaned_columns = [column for column in columns if column is not None]
        if cleaned_columns:
            self.data["group_by"] = cleaned_columns
        return self

    def order_by(self, *columns: Optional[Column]) -> Query:
        cleaned_columns = [column for column in columns if column is not None]
        if cleaned_columns:
            self.data["order_by"] = cleaned_columns
        return self

    def limit(self, value: int) -> Query:
        self._add_to_data("limit", "%d" % value)
        return self

    def offset(self, value: int) -> Query:
        self._add_to_data("offset", "%d" % value)
        return self

    def slice(self, start: int, stop: int) -> Query:
        return self.limit(stop - start).offset(start)

    def all(self):
        pass

    def first(self):
        pass

    def one_or_none(self):
        pass

    def exists(self):
        pass

    def count(self):
        pass

    def update(self, **fields_values):
        pass

    def delete(self):
        pass
