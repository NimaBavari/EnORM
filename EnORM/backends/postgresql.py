"""Contains datatypes to support PostgreSQL backend."""

import ipaddress
import json
from datetime import timedelta

import macaddress
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


class ARRAYMeta(type):
    @property
    def __name__(cls) -> str:
        return "ARRAY"

    def __instancecheck__(cls, instance) -> bool:
        return isinstance(instance, list)


class ARRAY(metaclass=ARRAYMeta):
    pass


class JSONBMeta(type):
    @property
    def __name__(cls) -> str:
        return "JSONB"

    def __instancecheck__(cls, instance) -> bool:
        try:
            _ = json.loads(instance)
        except json.JSONDecodeError:
            return False
        return True


class JSONB(metaclass=JSONBMeta):
    pass


class CIDRMeta(type):
    @property
    def __name__(cls) -> str:
        return "CIDR"

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, (ipaddress.IPv4Network, ipaddress.IPv6Network))


class CIDR(metaclass=CIDRMeta):
    pass


class MACADDRMeta(type):
    @property
    def __name__(cls) -> str:
        return "MACADDR"

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, macaddress.MAC)


class MACADDR(metaclass=MACADDRMeta):
    pass


class HSTOREMeta(type):
    @property
    def __name__(cls) -> str:
        return "HSTORE"

    def __instancecheck__(self, instance) -> bool:
        return isinstance(instance, dict)


class HSTORE(metaclass=HSTOREMeta):
    pass
