"""Contains definitions for custom exceptions."""

from typing import Any, Optional, Type


class IncompatibleArgument(TypeError):
    """Raised when parameters of incompatible values or incompatible types are used together."""


class EntityError(ValueError):
    """Raised when entities (column-like objects) are not used correctly."""


class MethodChainingError(ValueError):
    """Raised when a wrong sequence of methods are chained together on :class:`.query.Query`."""


class Fixed(Exception):
    """Base class for all messaged exceptions."""

    message: Optional[str] = None

    def __init__(self, *args: Any) -> None:
        super().__init__(self.message, *args)


class ValueOutOfBound(Fixed):
    """Raised when a value of an EnORM type is out of bounds."""

    def __init__(self, type_name: str) -> None:
        self.message = "`%s` value is out of bounds." % type_name
        super().__init__()


class FieldNotExist(Fixed):
    """Raised when the inquired field does not exist in a multi-field object."""

    def __init__(self, field_name: str) -> None:
        self.message = "Field name %s not exists." % field_name
        super().__init__()


class WrongFieldType(Fixed):
    """Raised when the value of a column is of another type than is declared."""

    def __init__(self, field_name: str, exp_type: Type, actual_type: Type) -> None:
        self.message = "Field %s expected %s but got %s." % (
            field_name,
            exp_type,
            actual_type,
        )
        super().__init__()


class MissingRequiredField(Fixed):
    """Raised when a new row is instantiated without a required field."""

    def __init__(self, field_name: str) -> None:
        self.message = "Cannot call without field %s." % field_name
        super().__init__()


class QueryFormatError(Fixed):
    """Raised when a query is formatted incorrectly."""

    message = "Wrong query format."


class MultipleResultsFound(Fixed):
    """Raised when multiple results are found while a single result is expected."""

    message = "Multiple results found."


class OrphanColumn(Fixed):
    """Raised when a column is instantiated outside a model definition."""

    message = "Cannot initialize `Column` outside a `Model`."
