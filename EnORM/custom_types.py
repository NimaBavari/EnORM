"""Contains definitions for frequently used composite types."""

from typing import Type, TypeAlias

from .column import BaseField
from .subquery import Subquery

QueryEntity: TypeAlias = Type | BaseField
BaseFieldRef: TypeAlias = BaseField | str
JoinEntity: TypeAlias = Type | Subquery
