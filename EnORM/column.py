from __future__ import annotations

from typing import Any, Iterable, Optional, Type, Union

from .exceptions import IncompatibleArgument
from .fkey import ForeignKey
from .types import Serial, String


class Label:
    """Docstring here."""

    def __init__(self, denotee: Union[Type, BaseColumn], text: str) -> None:
        self.denotee = denotee
        self.text = text


class BaseColumn:
    """Docstring here."""

    def __init__(self) -> None:
        self.compound_variable_name = "%s, %s" % (self.view_name, self.variable_name)

    def binary_ops(self, other: Any, operator: str) -> str:
        return "'%s'.'%s' %s %s" % (self.view_name, self.variable_name, operator, other)

    def __eq__(self, other: Any) -> str:
        return self.binary_ops(other, "=")

    def __ne__(self, other: Any) -> str:
        return self.binary_ops(other, "<>")

    def __lt__(self, other: Any) -> str:
        return self.binary_ops(other, "<")

    def __gt__(self, other: Any) -> str:
        return self.binary_ops(other, ">")

    def __le__(self, other: Any) -> str:
        return self.binary_ops(other, "<=")

    def __ge__(self, other: Any) -> str:
        return self.binary_ops(other, ">=")

    def like(self, other: str) -> str:
        return self.binary_ops(other, "LIKE")

    def in_(self, flat_list: Iterable[Any]) -> str:
        flat_list_str = "(%s)" % flat_list
        return self.binary_ops(flat_list_str, "IN")

    def not_in(self, flat_list: Iterable[Any]) -> str:
        flat_list_str = "(%s)" % flat_list
        return self.binary_ops(flat_list_str, "NOT IN")

    def label(self, alias: str) -> Label:
        return Label(self, alias)


class Column(BaseColumn):
    """Docstring here."""

    def __init__(
        self,
        type_: Type,
        length: Optional[int] = None,
        rel: Optional[ForeignKey] = None,
        *,
        primary_key: bool = False,
        default: Any = None,
        nullable: bool = True,
    ) -> None:
        self.type = type_
        self.length = length
        self.rel = rel
        self.primary_key = primary_key
        self.default = default
        self.nullable = nullable
        self.view_name = self.model.get_table_name()
        if self.primary_key and self.type not in [Serial, String]:
            raise IncompatibleArgument("Wrong type for primary key.")

        if self.rel is not None:
            if not isinstance(self.rel, ForeignKey):
                raise IncompatibleArgument("Relationship should be a `ForeignKey`.")

            if self.primary_key or self.default or not self.nullable:
                raise IncompatibleArgument("Wrong combination of arguments with `ForeignKey`.")

            if self.type not in [Serial, String]:
                raise IncompatibleArgument("Wrong type for `ForeignKey`.")

        if self.length is not None:
            if self.type != String:
                raise IncompatibleArgument("Only `String` type can have length.")

            if not isinstance(self.length, int):
                raise IncompatibleArgument("`String` type should have an integer length.")

        super().__init__()


class VirtualColumn(BaseColumn):
    """Docstring here."""

    def __init__(self, variable_name, view_name) -> None:
        self.variable_name = variable_name
        self.view_name = view_name
        super().__init__()
