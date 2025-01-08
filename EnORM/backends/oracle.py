"""Contains datatypes to support Oracle DB backend."""

from datetime import timedelta

from shapely.geometry.base import BaseGeometry


class GeometryMeta(type):
    @property
    def __name__(cls) -> str:
        return "Geometry"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, BaseGeometry)


class Geometry(metaclass=GeometryMeta):
    pass


class IntervalMeta(type):
    @property
    def __name__(cls) -> str:
        return "Interval"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, timedelta)


class Interval(metaclass=IntervalMeta):
    pass
