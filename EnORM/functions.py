"""Contains ORM functions, both aggregate and non-aggregate ones."""

from typing import Optional, Union

from .column import BaseColumn, Scalar


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


def char_length(c: Union[BaseColumn, str]) -> Scalar:
    full_field_name = c
    if isinstance(c, BaseColumn):
        full_field_name = ".".join(c.compound_variable_name.split(", "))
    return Scalar("CHAR_LENGTH(%s)" % full_field_name)


def concat(*parts: str) -> str:
    return "".join(parts)


def current_date() -> Scalar:
    return Scalar("CURRENT_DATE")


def current_time(precision: Optional[int] = None) -> Scalar:
    result = "CURRENT_TIME"
    if precision is not None:
        result += "(%d)" % precision
    return Scalar(result)


def current_timestamp(precision: Optional[int] = None) -> Scalar:
    result = "CURRENT_TIMESTAMP"
    if precision is not None:
        result += "(%d)" % precision
    return Scalar(result)


def current_user() -> Scalar:
    return Scalar("CURRENT_USER")


def local_time(precision: Optional[int] = None) -> Scalar:
    result = "LOCALTIME"
    if precision is not None:
        result += "(%d)" % precision
    return Scalar(result)


def local_timestamp() -> Scalar:
    return Scalar("LOCALTIMESTAMP")


def now() -> Scalar:
    return Scalar("NOW()")


def random() -> Scalar:
    return Scalar("RANDOM()")


def session_user() -> Scalar:
    return Scalar("SESSION_USER")


def user() -> Scalar:
    return Scalar("USER()")
