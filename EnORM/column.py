from __future__ import annotations

from typing import Any, Optional, Type, Union

from .types import ForeignKey, Integer, String


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
        rel: Optional[ForeignKey] = None,
        *,
        primary_key: bool = False,
        default: Any = None,
        nullable: bool = True
    ) -> None:
        self.type = type_
        self.rel = rel
        self.primary_key = primary_key
        self.default = default
        self.nullable = nullable
        if self.primary_key and self.type is not Integer:
            raise TypeError("Primary key should be an integer.")

        if self.rel:
            if not isinstance(self.rel, ForeignKey):
                raise TypeError("Relationship should be a ForeignKey.")

            if self.primary_key or self.default or not self.nullable:
                raise TypeError("Wrong combination of arguments with ForeignKey.")

            if self.type not in [Integer, String]:
                raise TypeError("Wrong type for ForeignKey.")

    def label(self, alias: str) -> Label:
        return Label(self, alias)
