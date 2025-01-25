"""Contains definitions for frequently used composite types."""

from typing import Type, TypeAlias

from .column import BaseColumn
from .subquery import Subquery

QueryEntity: TypeAlias = Type | BaseColumn
BaseColumnRef: TypeAlias = BaseColumn | str
JoinEntity: TypeAlias = Type | Subquery
