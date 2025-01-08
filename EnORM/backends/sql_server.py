"""Contains datatypes to support SQL Server backend."""

from shapely.geometry.base import BaseGeometry


class GeometryMeta(type):
    @property
    def __name__(cls) -> str:
        return "Geometry"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, BaseGeometry)


class Geometry(metaclass=GeometryMeta):
    pass
