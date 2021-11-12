from .structures import Key


class Column(Key):
    """Docstring here."""

    def __init__(self, type_, *, primary_key=False, default=False, nullable=False):
        self.type = type_
        self.primary_key = primary_key
        self.default = default
        self.nullable = nullable
        if self.primary_key and self.type is not int:
            raise TypeError("Primary key should be an integer.")


class ForeignKey(Key):
    """Docstring here."""

    pass
