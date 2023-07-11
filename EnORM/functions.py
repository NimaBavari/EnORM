from .column import BaseColumn


def agg(field: BaseColumn, name_in_sql: str) -> BaseColumn:
    v = field.compound_variable_name
    field.compound_variable_name = "%s(%s)" % (name_in_sql, v)
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