"""Contains definitions for custom types."""

from datetime import date, datetime, time

from .exceptions import ValueOutOfBound

Integer = int
Date = date
DateTime = datetime
Float = float
String = str
Time = time


class Serial(Integer):
    """ORM representation of serial types in SQL variants.

    :params val:    underlying integer value.

    Inherits from :class:`.types.Integer`.
    """

    def __init__(self, val: Integer) -> None:
        self.val = val
        if self.val < 1 or self.val > 2147483647:
            raise ValueOutOfBound("Serial")
