from __future__ import annotations

from typing import Any, Dict, Iterable, Optional, Type, Union

from .exceptions import IncompatibleArgument, OrphanColumn
from .fkey import ForeignKey
from .types import Serial, String


class Label:
    """Docstring here."""

    def __init__(self, denotee: Union[Type, BaseColumn], text: str) -> None:
        self.denotee = denotee
        self.text = text


class BaseColumn:
    """Docstring here."""

    def binary_ops(self, other: Any, operator: str) -> str:
        other_compound = "%s.%s" % (other.view_name, other.variable_name) if isinstance(other, BaseColumn) else other
        return "%s.%s %s %s" % (self.view_name, self.variable_name, operator, other_compound)

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

    @property
    def compound_variable_name(self) -> str:
        return "%s, %s" % (self.view_name, self.variable_name)


class Column(BaseColumn):
    """Docstring here."""

    objects: Dict[int, Dict[str, Any]] = {}

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

    @property
    def model(self) -> Type:
        try:
            m = self.objects[id(self)]["model"]
        except KeyError:
            raise OrphanColumn
        return m

    @property
    def variable_name(self) -> str:
        try:
            v = self.objects[id(self)]["variable_name"]
        except KeyError:
            raise OrphanColumn
        return v

    @property
    def view_name(self) -> str:
        return self.model.get_table_name()


class VirtualColumn(BaseColumn):
    """Docstring here."""

    def __init__(self, variable_name, view_name) -> None:
        self.variable_name = variable_name
        self.view_name = view_name
