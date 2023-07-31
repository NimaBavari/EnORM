"""Contains ORM functions, both aggregate and non-aggregate ones."""

from .column import BaseColumn


def agg(field: BaseColumn, name_in_sql: str) -> BaseColumn:
    field.aggs.append(name_in_sql)
    return field


def count(field: BaseColumn) -> BaseColumn:
    return agg(field, "COUNT")


def sum_(field: BaseColumn) -> BaseColumn:
    return agg(field, "SUM")


def avg(field: BaseColumn) -> BaseColumn:
    return agg(field, "AVG")


def min_(field: BaseColumn) -> BaseColumn:
    return agg(field, "MIN")


def max_(field: BaseColumn) -> BaseColumn:
    return agg(field, "MAX")
