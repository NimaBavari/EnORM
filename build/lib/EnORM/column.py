"""Module for containing the Column class."""

from typing import Any, AnyStr, NamedTuple


class Column(NamedTuple):
    """Creates a Column object.

        :params
            col_name    ->  name of the column in database table, as a string
            vartype     ->  type of the value the column holds in database
                            table, as a string
            max_l       ->  optional if vartype isn't 'varchar'; max allowed
                            length of the column value, as an integer;
                            defaults to None
            default     ->  optional; default value the column should have if
                            no value is given; defaults to None
            null        ->  optional; whether the column value is nullable, as
                            a boolean; defaults to True
            unique      ->  optional; whether the column value should be
                            unique, as a boolean; defaults to False
            p_key       ->  optional; whether the column is primary key, as a
                            boolean; defaults to False
            autoinc     ->  optional; whether the column value is auto-
                            incremented, as a boolean; defaults to False
    """

    col_name: AnyStr
    vartype: AnyStr
    max_l: 'int' = None
    default: Any = None
    null: 'bool' = True
    unique: 'bool' = False
    p_key: 'bool' = False
    autoinc: 'bool' = False
