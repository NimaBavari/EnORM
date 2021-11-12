from __future__ import annotations

from typing import Type, Union


class Label:
    """Docstring here."""

    def __init__(self, denotee: Union[Type, Key], text: str) -> None:
        self.denotee = denotee
        self.text = text


class Key:
    """Docstring here."""

    def label(self, alias: str) -> Label:
        return Label(self, alias)


class Record:
    """Docstring here."""

    pass
