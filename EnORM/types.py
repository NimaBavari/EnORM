from .exceptions import ValueOutOfBound

Integer = int
Float = float
String = str


class Serial(Integer):
    """Docstring here."""

    def __init__(self, val: Integer) -> None:
        self.val = val
        if self.val < 1 or self.val > 2147483647:
            raise ValueOutOfBound("Serial")
