"""Contains definitions for custom types."""

from .exceptions import ValueOutOfBound

Integer = int
Float = float
String = str


class Serial(Integer):
    """Representer of serial type in SQL variants.

    :params val:    underlying integer value.

    Inherits from :class:`.types.Integer`.
    """

    def __init__(self, val: Integer) -> None:
        self.val = val
        if self.val < 1 or self.val > 2147483647:
            raise ValueOutOfBound("Serial")
