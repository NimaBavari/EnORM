from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional, Type, Union

from .column import Column, Label
from .database import DBSession
from .model import Model


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

    def __init__(self, lst: List[Record]):
        self.lst = lst

    def __iter__(self) -> Iterator[Record]:
        yield from self.lst

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


class Query:
    """Docstring here."""

    def __init__(self, *entities: Union[Type, Column, Label], session: DBSession) -> None:
        # NOTE: When `all`, `one`, etc. methods (the final methods) are
        # implemented, we need to convert the list of tuples into the list of
        # `Record` objects.
        #
        # `Record` object is a `MappedClass` object if the only entity in
        # `entities` is `MappedClass` (annotated with `Type`); otherwise, it
        # is a `Record` of pure tuple containing the other entities, each
        # attributed to the `MappedClass`. Note that, `MappedClass` is any
        # subclass of `Model`.
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
                        next(key for key, val in item.model.__dict__.items() if val is item),
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
                            next(key for key, val in denotee.model.__dict__.items() if val is item),
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

    def filter(self, *exprs: Any) -> Query:
        for expr in exprs:
            self._add_to_data("where", expr)

        return self

    def filter_by(self, **kwcrts: Any) -> Query:
        criteria = [eval("%s.%s == %s") % (self.mapped_class.__name__, key, val) for key, val in kwcrts.items()]
        return self.filter(*criteria)

    def join(self, model_cls: Type) -> Query:
        # TODO: Implement. Note that this is very complicated.
        return self

    def having(self, expr: Any) -> Query:
        self._add_to_data("having", expr)
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

    def get(self, **kwargs: Any) -> Optional[Record]:
        if "where" in self.data and self.data["where"]:
            raise ValueError("Cannot use `get` after `filter` or `filter_by`.")

        query_set = self.filter_by(**kwargs).all()
        if len(query_set) > 1:
            raise ValueError("Multiple results found.")

        return query_set[0] if query_set else None

    def all(self) -> QuerySet:
        pass

    def first(self) -> Optional[Record]:
        try:
            (result,) = self.limit(1).all()
        except ValueError:
            return None

        return result

    def one_or_none(self) -> Optional[Record]:
        query_set = self.all()
        if len(query_set) > 1:
            raise ValueError("Multiple results found.")

        return query_set[0] if query_set else None

    def exists(self) -> bool:
        return bool(self.first())

    def count(self) -> int:
        pass

    def update(self, **fields_values) -> None:
        # TODO: Implement this!
        """Two ways of updates:
            1. `user = session.query(User).filter(User.username == "nbavari").first()` and then `user.age += 1`
            2. `session.query(User).filter(User.username == "nbavari").update(**field_values)`
        You have to put `session.save()` after both to persist it.
        """

    def delete(self) -> None:
        # TODO: Implement this!
        """Example usage:
        ```
        session.query(User).filter(User.username == "nbavari").delete()
        session.save()
        ```
        """
