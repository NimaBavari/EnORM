"""Contains basic datatypes."""

from datetime import date, datetime, time
from decimal import Decimal

from ..exceptions import ValueOutOfBound


class IntegerMeta(type):
    @property
    def __name__(cls) -> str:
        return "Integer"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, int)


class Integer(metaclass=IntegerMeta):
    pass


class BooleanMeta(type):
    @property
    def __name__(cls) -> str:
        return "Boolean"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, bool)


class Boolean(metaclass=BooleanMeta):
    pass


class FloatMeta(type):
    @property
    def __name__(cls) -> str:
        return "Float"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, float)


class Float(metaclass=FloatMeta):
    pass


class NumericMeta(type):
    @property
    def __name__(cls) -> str:
        return "Numeric"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, Decimal)


class Numeric(metaclass=NumericMeta):
    pass


class StringMeta(type):
    @property
    def __name__(cls) -> str:
        return "String"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, str)


class String(metaclass=StringMeta):
    pass


class DateMeta(type):
    @property
    def __name__(cls) -> str:
        return "Date"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, date)


class Date(metaclass=DateMeta):
    pass


class TimeMeta(type):
    @property
    def __name__(cls) -> str:
        return "Time"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, time)


class Time(metaclass=TimeMeta):
    pass


class DateTimeMeta(type):
    @property
    def __name__(cls) -> str:
        return "DateTime"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, datetime)


class DateTime(metaclass=DateTimeMeta):
    pass


class BinaryMeta(type):
    @property
    def __name__(cls) -> str:
        return "Binary"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, bytes)


class Binary(metaclass=BinaryMeta):
    pass


class Serial(Integer):
    """ORM representation of serial types in SQL variants. Inherits from :class:`.types.Integer`.

    :params val:    underlying integer value.
    """

    def __init__(self, val: Integer) -> None:
        self.val = val
        if self.val < 1 or self.val > 2147483647:
            raise ValueOutOfBound("Serial")
