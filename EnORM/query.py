"""Contains :class:`.query.Query` and :class:`.query.Subquery`.

Also contains the class for complete and incomplete row-like objects, namely, :class:`.query.Record` and the class for
any collection of them :class:`.query.QuerySet`.
"""

from __future__ import annotations

from collections import UserDict
from typing import Any, Dict, Iterator, List, Optional, Type, Union

import pyodbc

from .column import BaseColumn, Column, Label, VirtualColumn
from .db_engine import DBEngine
from .exceptions import EntityError, FieldNotExist, MethodChainingError, MultipleResultsFound, QueryFormatError


class Record(UserDict):
    """Docstring here."""

    def __init__(self, d: Dict[str, Any], query: Query) -> None:
        super().__init__(d)
        self.query = query

    def __getattr__(self, attr: str) -> Any:
        try:
            return self[attr]
        except KeyError as e:
            if self.is_row:
                try:
                    self_model = self.query.entities[0].denotee
                except AttributeError:
                    self_model = self.query.entities[0]

                for m in self_model.__dep_mapping[self_model]:
                    connector = m.get_connector_column(self_model)
                    if connector.rel.reverse_name == attr:
                        condition_dict = {
                            connector.variable_name: getattr(self, self_model.get_primary_key_column().variable_name)
                        }
                        return Query(m).join(self_model).filter_by(**condition_dict).subquery()

            raise FieldNotExist(attr) from e

    def __setattr__(self, attr: str, value: Any) -> None:
        if attr not in self:
            raise FieldNotExist(attr)

        self.query.filter_by(**self).update(**{attr: value})

    @property
    def is_row(self) -> bool:
        return len(self.query.entities) == 1 and (
            isinstance(self.query.entities[0], type)
            or (isinstance(self.query.entities[0], Label) and isinstance(self.query.entities[0].denotee, type))
        )


class QuerySet:
    """Docstring here."""

    def __init__(self, lst: List[Record]) -> None:
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


class Subquery:
    """Representer of an SQL subquery.

    A subquery is a nested SELECT statement that is used within another SQL statement.

    :params inner_sql:      SQL string of the view represented by the subquery
    :params column_names:   Original names of the columns in that view.

    Never directly instantiated, but rather initialised by invoking :meth:`.query.Query.subquery()`.
    """

    subquery_idx = 0

    def __init__(self, inner_sql: str, column_names: List[str]) -> None:
        type(self).subquery_idx += 1
        self.inner_sql = inner_sql
        self.column_names = column_names
        self.view_name = "anon_%d" % self.subquery_idx
        self.full_sql = "(%s) AS %s" % (self.inner_sql, self.view_name)

    def __str__(self) -> str:
        return self.inner_sql

    def __getattr__(self, attr: str) -> Any:
        if attr not in self.column_names:
            raise EntityError("Wrong field for subquery.")

        return VirtualColumn(attr, self.view_name)


class Query:
    """Main abstraction for querying for the whole ORM.

    There are two ways to generate :class:`.query.Query` objects: either by calling the
    :meth:`.db_session.DBSession.query` method, which is the most usual way, or, less commonly, by instantiating
    :class:`.query.Query` directly.

    Gets as an argument the

    :param entities: -- which correspond to the "columns" of the matched results.

    .. warning::

    :param entities: may contain at most one `MappedClass` instance.

    NOTE that `MappedClass` is any subclass of :class:`.model.Model`.
    """

    def __init__(self, *entities: Union[Type, BaseColumn, Label]) -> None:
        self.entities = entities
        self.data: Dict[str, List[Any]] = {}
        if not self.entities:
            raise EntityError("No fields specified for querying.")

        if sum(isinstance(item, type) for item in self.entities) > 1:
            raise EntityError("More than one model specified in the query.")

        for item in self.entities:
            if isinstance(item, type):
                self.mapped_class = item
                table_name = item.get_table_name()
                self._add_to_data("select", "%s, *" % table_name)
                self._add_to_data("from", table_name)
            elif isinstance(item, BaseColumn):
                self._add_to_data("select", item.compound_variable_name)
                if isinstance(item, Column):
                    self._add_to_data("from", item.view_name)
            elif isinstance(item, Label):
                if isinstance(item.denotee, type):
                    table_name = item.denotee.get_table_name()
                    self._add_to_data("select", "%s, *" % table_name)
                    self._add_to_data("from", table_name)
                    self._add_to_data("from_as", item.text)
                elif isinstance(item.denotee, BaseColumn):
                    comp_name = ", ".join([item.denotee.compound_variable_name, item.text, *item.denotee.aggs])
                    item.denotee.aggs = []
                    self._add_to_data("select", comp_name)
                    if isinstance(item.denotee, Column):
                        self._add_to_data("from", item.denotee.view_name)
            else:
                raise QueryFormatError

    def __str__(self) -> str:
        return self._sql

    def _add_to_data(self, key: str, val: str) -> None:
        """Appends a value to the list `self.data[key]`.

        If `key` does not exist in `self.data`, instantiates it as an empty list and append to it.
        """
        self.data[key] = [*self.data.get(key, []), val]

    @property
    def _sql(self) -> str:
        """Gets the SQL representation of the current query.

        :return: valid SQL string.
        """
        return self.parse()

    def join(self, mapped: Union[Type, Subquery], *exprs: Any) -> Query:
        self_model = self.mapped_class or self.entities[0].model
        if isinstance(mapped, type):
            connector_column = self_model.get_connector_column(mapped)
            if connector_column is None:
                raise EntityError("No connector key found between %s and %s." % (self_model.__name__, mapped.__name__))

            self._add_to_data("join", mapped.get_table_name())
            if exprs:
                self.data["on"] = exprs
            else:
                exec("from %s import %s" % (self_model.__module__, self_model.__name__), globals(), globals())
                exec("from %s import %s" % (mapped.__module__, mapped.__name__), globals(), globals())
                expr = eval(
                    "%s.%s == %s.%s"
                    % (
                        self_model.__name__,
                        connector_column.variable_name,
                        mapped.__name__,
                        mapped.get_primary_key_column().variable_name,
                    )
                )
                self._add_to_data("on", expr)
        elif isinstance(mapped, Subquery):
            if not exprs:
                raise EntityError("Cannot join subquery without connector expressions.")
            self._add_to_data("join", mapped.full_sql)
            self.data["on"] = exprs

        return self

    def filter(self, *exprs: Any) -> Query:
        """Exerts a series of valid comparison expressions as filtering criteria to the current instance.

        E.g.::

            session.query(User, email_address, last_visited)
                .filter(User.first_name == "Nima", User.age > 28)
                .first()

        Any number of criteria may be specified as separated by a comma.

        .. seealso::

            :meth:`.query.Query.filter_by` - filter on keyword arguments as criteria.
        """
        for expr in exprs:
            self._add_to_data("where", expr)

        return self

    def filter_by(self, **kwcrts: Any) -> Query:
        """Exerts a series of keyword arguments as filtering criteria to the current instance.

        E.g.::

            session.query(Employee, full_name, salary, tenure)
                .filter_by(department="Information Technologies", status="active")
                .all()

        Any number of criteria may be specified as separated by a comma.

        .. seealso::

            :meth:`.query.Query.filter` - filter on valid comparison expressions as criteria.
        """
        model = self.mapped_class or self.entities[0].model
        exec("from %s import %s" % (model.__module__, model.__name__), globals(), globals())
        criteria = [eval("%s.%s == '%s'" % (model.__name__, key, val)) for key, val in kwcrts.items()]
        return self.filter(*criteria)

    def group_by(self, *columns: Union[BaseColumn, str]) -> Query:
        column_names = [
            column.compound_variable_name if isinstance(column, BaseColumn) else column for column in columns
        ]
        if column_names:
            self.data["group_by"] = column_names

        return self

    def having(self, expr: Any) -> Query:
        self._add_to_data("having", expr)
        return self

    def order_by(self, *columns: Union[BaseColumn, str]) -> Query:
        column_names = [
            column.compound_variable_name if isinstance(column, BaseColumn) else column for column in columns
        ]
        if column_names:
            self.data["order_by"] = column_names

        return self

    def limit(self, value: int) -> Query:
        self._add_to_data("limit", "%d" % value)
        return self

    def offset(self, value: int) -> Query:
        self._add_to_data("offset", "%d" % value)
        return self

    def slice(self, start: int, stop: int) -> Query:
        return self.limit(stop - start).offset(start)

    def desc(self) -> Query:
        if "order_by" not in self.data or not self.data["order_by"]:
            raise MethodChainingError("Cannot use `desc` without `order_by`.")

        self.data["desc"] = []

        return self

    def distinct(self) -> Query:
        self.data["distinct"] = []
        return self

    def subquery(self) -> Subquery:
        column_names = [s.split(", ")[1] for s in self.data["select"]]
        return Subquery(self._sql, column_names)

    def get(self, **kwargs: Any) -> Optional[Record]:
        if "where" in self.data and self.data["where"]:
            raise MethodChainingError("Cannot use `get` after `filter` or `filter_by`.")

        query_set = self.filter_by(**kwargs).all()
        if len(query_set) > 1:
            raise MultipleResultsFound

        return query_set[0] if query_set else None

    def all(self) -> QuerySet:
        engine = DBEngine.active_instance
        try:
            engine.cursor.execute(self._sql)
            col_names = [col[0] for col in engine.cursor.description]
            results = [Record(dict(zip(col_names, row)), self) for row in engine.cursor.fetchall()]
        except pyodbc.DatabaseError:
            raise QueryFormatError

        return QuerySet(results)

    def first(self) -> Optional[Record]:
        (result,) = self.limit(1).all()
        return result

    def one_or_none(self) -> Optional[Record]:
        query_set = self.all()
        if len(query_set) > 1:
            raise MultipleResultsFound

        return query_set[0] if query_set else None

    def exists(self) -> bool:
        return bool(self.first())

    def count(self) -> int:
        results = self.all()

        return len(results)

    def update(self, **fields_values) -> None:
        """Two ways of updates:
            1. `user = session.query(User).filter(User.username == "nbavari").first()` and then `user.age += 1`
            2. `session.query(User).filter(User.username == "nbavari").update(**field_values)`
        You have to put `session.save()` after both to persist it.
        """
        self.data["update"] = self.data.pop("select")
        self.data["set"] = list(fields_values.items())

    def delete(self) -> None:
        """Example usage:
        ```
        session.query(User).filter(User.username == "nbavari").delete()
        session.save()
        ```
        """
        self.data["delete"] = self.data.pop("select")

    def parse(self) -> str:
        def parse_item(compound_name: str) -> str:
            parts = compound_name.split(", ")
            if len(parts) == 2:
                return "%s.%s" % (*parts,)
            if len(parts) == 3:
                return "%s.%s AS %s" % (*parts,)
            incomplete_res = "%s.%s" % (parts[0], parts[1])
            for part in parts[:2:-1]:
                incomplete_res = "%s(%s)" % (part, incomplete_res)
            return "%s AS %s" % (incomplete_res, parts[2])

        parsed_str = ""
        if "select" in self.data:
            table = self.data["from"][0]

            to_remove = "%s, *" % table
            if len(self.data["select"]) > 1 and to_remove in self.data["select"]:
                self.data["select"].remove(to_remove)

            column_seq = ", ".join(parse_item(s) for s in self.data["select"])

            if "distinct" in self.data:
                column_seq = "DISTINCT %s" % column_seq
            parsed_str += "SELECT %s FROM %s" % (column_seq, table)
        elif "delete" in self.data:
            table = self.data["from"][0]
            parsed_str = "DELETE FROM %s" % table
        elif "update" in self.data:
            table = self.data["update"][0].get_table_name()
            fields_values_seq = ", ".join("%s = %s" % (field, value) for field, value in self.data["set"])
            parsed_str = "UPDATE %s SET %s" % (table, fields_values_seq)

        if "from_as" in self.data:
            parsed_str += " AS %s" % self.data["from_as"][0]

        if "join" in self.data:
            condition = " AND ".join(expr for expr in self.data["on"])
            parsed_str += " JOIN %s ON %s" % (self.data["join"][0], condition)

        if "where" in self.data:
            condition = " AND ".join(expr for expr in self.data["where"])
            parsed_str += " WHERE %s" % condition

        if "group_by" in self.data:
            column_name_seq = ", ".join(
                name if len(name.split(", ")) == 1 else "%s.%s" % (*name.split(", "),) for name in self.data["group_by"]
            )
            parsed_str += " GROUP BY %s" % column_name_seq

        if "having" in self.data:
            condition = " AND ".join(expr for expr in self.data["having"])
            parsed_str += " HAVING %s" % condition

        if "order_by" in self.data:
            column_name_seq = ", ".join(
                name if len(name.split(", ")) == 1 else "%s.%s" % (*name.split(", "),) for name in self.data["order_by"]
            )
            parsed_str += " ORDER BY %s" % column_name_seq

        if "limit" in self.data:
            parsed_str += " LIMIT %s" % self.data["limit"][0]

        if "offset" in self.data:
            parsed_str += " OFFSET %s" % self.data["offset"][0]

        if "desc" in self.data:
            parsed_str += " DESC"

        return parsed_str
