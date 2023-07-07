from __future__ import annotations

from typing import Any, Optional, Type, Union

from .exceptions import IncompatibleArgument
from .types import Serial, String

CASCADE = "cascade"


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
                raise IncompatibleArgument("Relationship should be a ForeignKey.")

            if self.primary_key or self.default or not self.nullable:
                raise IncompatibleArgument("Wrong combination of arguments with ForeignKey.")

            if self.type not in [Serial, String]:
                raise IncompatibleArgument("Wrong type for ForeignKey.")

        if self.length is not None:
            if self.type != String:
                raise IncompatibleArgument("Only String type can have length.")

            if not isinstance(self.length, int):
                raise IncompatibleArgument("String type should have an integer length.")

    def binary_ops(self, other: Any, operator: str) -> str:
        return "'%s'.'%s' %s %s" % (
            self.model.__name__,
            self.variable_name,
            operator,
            other,
        )

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

    def like(self, other: str) -> str:
        return self.binary_ops(other, "LIKE")

    def label(self, alias: str) -> Label:
        return Label(self, alias)

    def in_(self, smth: Any) -> str:
        # TODO: Implement this! Signature is wrong.
        return ""

    def not_in(self, smth: Any) -> str:
        # TODO: Implement this! Signature is wrong.
        return ""


class ForeignKey:
    """Docstring here."""

    def __init__(
        self,
        foreign_model: Type,
        *,
        reverse_name: str,
        on_delete: Optional[str] = None,
        on_update: Optional[str] = None,
    ) -> None:
        self.foreign_model = foreign_model
        self.reverse_name = reverse_name
        self.on_delete = on_delete
        self.on_update = on_update
        if self.on_delete not in [None, CASCADE]:
            raise IncompatibleArgument("Wrong value for on_delete")
        if self.on_update not in [None, CASCADE]:
            raise IncompatibleArgument("Wrong value for on_update")
