from __future__ import annotations

from typing import Any, Dict

from .tags import Key, Label
from .types import String


class Model:
    """Docstring here."""

    __table__ = None
    __TYPES = {
        # TODO: Fill this with type conversions
        int: "INTEGER",
        String: "VARCHAR",
    }

    def __new__(cls, *args: Any, **kwargs: Any) -> Model:
        fields = cls.get_fields()
        tablename = cls.get_table_name()
        query = """DROP TABLE %s IF EXISTS;
        CREATE TABLE %s (%s);""" % (
            tablename,
            tablename,
            ", ".join([cls.get_type_pref(field, val) for field, val in fields.items()]),
        )
        # TODO: get session somehow (without having to pass it as an argument)
        # then `session._cursor.execute(query)`
        return super().__new__(cls)

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        fields = cls.get_fields()
        for v in fields.values():
            v.model = cls

    def __init__(self, **attrs: Any) -> None:
        self.attrs = attrs
        fields = self.get_fields()
        for key, value in self.attrs.items():
            if key not in fields.keys():
                raise ValueError("Field name %s not exists." % key)
            expected_type = fields[key].type
            if not isinstance(value, expected_type):
                raise TypeError("Field name %s expected %s but got %s" % (key, expected_type, type(value)))
        for field, value in fields.items():
            if field in self.attrs.keys():
                continue
            if field == "id":
                continue
            if value.nullable:
                continue
            if value.default:
                continue
            raise ValueError("Cannot call without field name %s" % field)

    @classmethod
    def get_fields(cls) -> Dict[str, Key]:
        return {key: val for key, val in cls.__dict__.items() if not key.startswith("__") and not callable(key)}

    @classmethod
    def get_table_name(cls) -> str:
        return cls.__table__ or "%ss" % cls.__qualname__.lower()

    @classmethod
    def get_type_pref(cls, field: str, val: Key) -> str:
        # TODO: add foreign key logic too
        type_pref = cls.__TYPES[val.type]
        if val.type.length is not None:
            type_pref += " %d" % val.type.length
        if val.primary_key:
            type_pref += " AUTOINCREMENT PRIMARY KEY"
        return "%s %s" % (field, type_pref)

    @classmethod
    def label(cls, alias: str) -> Label:
        return Label(cls, alias)

    @property
    def sql(self) -> str:
        return """INSERT INTO %s (%s) VALUES (%s);""" % (
            self.get_table_name(),
            ", ".join(self.attrs.keys()),
            ", ".join(["?" for _ in self.attrs]),
        )
