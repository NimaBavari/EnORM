from __future__ import annotations

from typing import Any, Dict

from .column import Column, Label
from .types import Float, Integer, Serial, String


class Model:
    """Docstring here."""

    __table__ = None
    __TYPES = {
        Integer: "INTEGER",
        String: "VARCHAR",
        Float: "NUMERIC",
        Serial: "SERIAL",
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
        for field, val in fields.items():
            val.model = cls
            val.variable_name = field

    def __init__(self, **attrs: Any) -> None:
        self.attrs = attrs

        fields = self.get_fields()
        for key, val in self.attrs.items():
            if key not in fields.keys():
                raise ValueError("Field name %s not exists." % key)

            expected_type = fields[key].type
            if not isinstance(val, expected_type):
                raise TypeError("Field name %s expected %s but got %s" % (key, expected_type, type(val)))

        for field, val in fields.items():
            if field in self.attrs.keys():
                continue

            if field == "id":
                continue

            if val.nullable:
                continue

            if val.default:
                continue

            raise ValueError("Cannot call without field name %s" % field)

    @classmethod
    def get_fields(cls) -> Dict[str, Column]:
        return {key: val for key, val in cls.__dict__.items() if not key.startswith("__") and not callable(key)}

    @classmethod
    def get_table_name(cls) -> str:
        return cls.__table__ or "%ss" % cls.__qualname__.lower()

    @classmethod
    def get_type_pref(cls, field: str, val: Column) -> str:
        type_pref = cls.__TYPES[val.type]
        if val.length is not None:
            type_pref += " (%d)" % val.length
        elif val.type == String:
            type_pref = "TEXT"

        if val.primary_key:
            if val.type == Serial:
                type_pref += " AUTOINCREMENT"
            type_pref += " PRIMARY KEY"

        if val.default:
            type_pref += " DEFAULT %s" % val.default

        if not val.nullable:
            type_pref += " NOT NULL"

        if val.rel:
            pass  # TODO: add foreign key logic too

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
