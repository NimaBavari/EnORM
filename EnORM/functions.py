"""Contains ORM functions, both aggregate and non-aggregate ones."""

from typing import Optional, Union

from .column import BaseColumn, Scalar


def agg(field: BaseColumn, name_in_sql: str) -> BaseColumn:
    """Describes the basis for all aggregate functions."""
    field.aggs.append(name_in_sql)
    return field


def count(field: BaseColumn) -> BaseColumn:
    """Describes the SQL aggregate function `COUNT`."""
    return agg(field, "COUNT")


def sum_(field: BaseColumn) -> BaseColumn:
    """Describes the SQL aggregate function `SUM`."""
    return agg(field, "SUM")


def avg(field: BaseColumn) -> BaseColumn:
    """Describes the SQL aggregate function `AVG`."""
    return agg(field, "AVG")


def min_(field: BaseColumn) -> BaseColumn:
    """Describes the SQL aggregate function `MIN`."""
    return agg(field, "MIN")


def max_(field: BaseColumn) -> BaseColumn:
    """Describes the SQL aggregate function `MAX`."""
    return agg(field, "MAX")


def char_length(c: Union[BaseColumn, str]) -> Scalar:
    """Describes the SQL function `CHAR_LENGTH`."""
    full_field_name = c
    if isinstance(c, BaseColumn):
        full_field_name = ".".join(c.compound_variable_name.split(", "))
    return Scalar("CHAR_LENGTH(%s)" % full_field_name)


def concat(*parts: str) -> str:
    """Concatenates multiple strings into one."""
    return "".join(parts)


def current_date() -> Scalar:
    """Describes the SQL function `CURRENT_DATE`."""
    return Scalar("CURRENT_DATE")


def current_time(precision: Optional[int] = None) -> Scalar:
    """Describes the SQL function `CURRENT_TIME`."""
    result = "CURRENT_TIME"
    if precision is not None:
        result += "(%d)" % precision
    return Scalar(result)


def current_timestamp(precision: Optional[int] = None) -> Scalar:
    """Describes the SQL function `CURRENT_TIMESTAMP`."""
    result = "CURRENT_TIMESTAMP"
    if precision is not None:
        result += "(%d)" % precision
    return Scalar(result)


def current_user() -> Scalar:
    """Describes the SQL function `CURRENT_USER`."""
    return Scalar("CURRENT_USER")


def local_time(precision: Optional[int] = None) -> Scalar:
    """Describes the SQL function `LOCALTIME`."""
    result = "LOCALTIME"
    if precision is not None:
        result += "(%d)" % precision
    return Scalar(result)


def local_timestamp() -> Scalar:
    """Describes the SQL function `LOCALTIMESTAMP`."""
    return Scalar("LOCALTIMESTAMP")


def now() -> Scalar:
    """Describes the SQL function `NOW`."""
    return Scalar("NOW()")


def random() -> Scalar:
    """Describes the SQL function `RANDOM`."""
    return Scalar("RANDOM()")


def session_user() -> Scalar:
    """Describes the SQL function `SESSION_USER`."""
    return Scalar("SESSION_USER")


def user() -> Scalar:
    """Describes the SQL function `USER`."""
    return Scalar("USER()")
