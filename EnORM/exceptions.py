from typing import Any, Optional, Type


class IncompatibleArgument(TypeError):
    """Docstring here."""


class EntityError(ValueError):
    """Docstring here."""


class MethodChainingError(ValueError):
    """Docstring here."""


class Fixed(Exception):
    """Docstring here."""

    message: Optional[str] = None

    def __init__(self, *args: Any) -> None:
        super().__init__(self.message, *args)


class ValueOutOfBound(Fixed):
    """Docstring here."""

    def __init__(self, type_name: str) -> None:
        self.message = "%s value is out of bounds." % type_name
        super().__init__()


class FieldNotExist(Fixed):
    """Docstring here."""

    def __init__(self, field_name: str) -> None:
        self.message = "Field name %s not exists." % field_name
        super().__init__()


class WrongFieldType(Fixed):
    """Docstring here."""

    def __init__(self, field_name: str, exp_type: Type, actual_type: Type) -> None:
        self.message = "Field %s expected %s but got %s." % (
            field_name,
            exp_type,
            actual_type,
        )
        super().__init__()


class MissingRequiredField(Fixed):
    """Docstring here."""

    def __init__(self, field_name: str) -> None:
        self.message = "Cannot call without field %s." % field_name
        super().__init__()


class QueryFormatError(Fixed):
    """Docstring here."""

    message = "Wrong query format."


class MultipleResultsFound(Fixed):
    """Docstring here."""

    message = "Multiple results found."
