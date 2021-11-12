from typing import Optional

Integer = int
Float = float


class String(str):
    """Docstring here."""

    def __init__(self, length: Optional[int] = None):
        self.length = length
        if self.length is not None and not isinstance(self.length, Integer):
            raise TypeError("String type should have an integer length.")


class ForeignKey:
    """Docstring here."""
