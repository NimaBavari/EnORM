from __future__ import annotations

from typing import Any, Optional, Type, Union

from .types import Serial, String


class Label:
    """Docstring here."""

    def __init__(self, denotee: Union[Type, Column], text: str) -> None:
        self.denotee = denotee
        self.text = text


class Column:
    """Docstring here."""

    def __init__(
        self,
        type_: Type,
        length: Optional[int] = None,
        rel: Optional[ForeignKey] = None,
        *,
        primary_key: bool = False,
        default: Any = None,
        nullable: bool = True
    ) -> None:
        self.type = type_
        self.rel = rel
        self.length = length
        self.primary_key = primary_key
        self.default = default
        self.nullable = nullable
        if self.primary_key and self.type not in [Serial, String]:
            raise TypeError("Wrong type for primary key.")

        if self.rel is not None:
            if not isinstance(self.rel, ForeignKey):
                raise TypeError("Relationship should be a ForeignKey.")

            if self.primary_key or self.default or not self.nullable:
                raise TypeError("Wrong combination of arguments with ForeignKey.")

            if self.type not in [Serial, String]:
                raise TypeError("Wrong type for ForeignKey.")

        if self.length is not None:
            if self.type != String:
                raise TypeError("Only String type can have length.")

            if not isinstance(self.length, int):
                raise TypeError("String type should have an integer length.")

    def binary_ops(self, other: Any, operator: str) -> str:
        return "'%s'.'%s' %s %s" % (self.model.__name__, self.variable_name, operator, other)

    def __eq__(self, other: Any) -> str:  # type: ignore
        return self.binary_ops(other, "=")

    def __ne__(self, other: Any) -> str:  # type: ignore
        return self.binary_ops(other, "<>")

    def __lt__(self, other: Any) -> str:
        return self.binary_ops(other, "<")

    def __gt__(self, other: Any) -> str:
        return self.binary_ops(other, ">")

    def __le__(self, other: Any) -> str:
        return self.binary_ops(other, "<=")

    def __ge__(self, other: Any) -> str:
        return self.binary_ops(other, ">=")

    def label(self, alias: str) -> Label:
        return Label(self, alias)


class ForeignKey:
    """Docstring here."""
