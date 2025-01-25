"""Contains :class:`.subquery.Subquery` and its helpers."""

from typing import Any, List

from .column import VirtualField
from .exceptions import EntityError


class Subquery:
    """Representer of an SQL subquery.

    A subquery is a nested SELECT statement that is used within another SQL statement.

    Never directly instantiated, but rather initialised by invoking :meth:`.query.Query.subquery()`.

    :param inner_sql:       SQL string of the view represented by the subquery
    :param column_names:    original names of the columns in that view.
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

        return VirtualField(attr, self.view_name)
