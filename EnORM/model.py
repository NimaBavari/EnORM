from __future__ import annotations

from typing import Any, Dict

from .column import Column, Label
from .exceptions import FieldNotExist, MissingRequiredField, WrongFieldType
from .types import Float, Integer, Serial, String

defined_model_qs = []


class Model:
    """Docstring here."""

    __table__ = None
    __TYPES = {
        Integer: "INTEGER",
        String: "VARCHAR",
        Float: "NUMERIC",
        Serial: "SERIAL",
    }

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        fields = cls.get_fields()
        tablename = cls.get_table_name()
        query = """DROP TABLE %s IF EXISTS; CREATE TABLE %s (%s);""" % (
            tablename,
            tablename,
            ", ".join(cls.get_type_pref(field, val) for field, val in fields.items()),
        )
        defined_model_qs.append(query)
        for field, val in fields.items():
            val.model = cls
            val.variable_name = field

    def __init__(self, **attrs: Any) -> None:
        self.attrs = attrs

        fields = self.get_fields()
        for key, val in self.attrs.items():
            if key not in fields.keys():
                raise FieldNotExist(key)

            expected_type = fields[key].type
            if not isinstance(val, expected_type):
                raise WrongFieldType(key, expected_type, type(val))

        for field, val in fields.items():
            if field in self.attrs.keys():
                continue

            if field == "id":
                continue

            if val.nullable:
                continue

            if val.default:
                continue

            raise MissingRequiredField(field)

    @classmethod
    def get_fields(cls) -> Dict[str, Column]:
        return {key: val for key, val in cls.__dict__.items() if not key.startswith("__") and not callable(key)}

    @classmethod
    def get_table_name(cls) -> str:
        return cls.__table__ or "%ss" % cls.__qualname__.lower()

    @classmethod
    def primary_key_col_name(cls) -> str:
        fields = cls.get_fields()
        for field, val in fields.items():
            if val.primary_key:
                return field
        return "id"

    @classmethod
    def get_type_pref(cls, field: str, val: Column) -> str:
        type_pref_inc = cls.__TYPES[val.type]
        if val.rel is not None:
            pref = "%s %s FOREIGN KEY (%s) REFERENCES %s(%s)" % (
                field,
                type_pref_inc,
                field,
                val.rel.foreign_model.__name__,
                val.rel.foreign_model.primary_key_col_name(),
            )
            if val.rel.on_delete is not None:
                pref += " ON DELETE CASCADE"
            if val.rel.on_update is not None:
                pref += " ON UPDATE CASCADE"
            return pref

        if val.length is not None:
            type_pref_inc += " (%d)" % val.length
        elif val.type == String:
            type_pref_inc = "TEXT"

        if val.primary_key:
            if val.type == Serial:
                type_pref_inc += " AUTOINCREMENT"
            type_pref_inc += " PRIMARY KEY"

        if val.default:
            type_pref_inc += " DEFAULT %s" % val.default

        if not val.nullable:
            type_pref_inc += " NOT NULL"

        return "%s %s" % (field, type_pref_inc)

    @classmethod
    def label(cls, alias: str) -> Label:
        return Label(cls, alias)

    @property
    def sql(self) -> str:
        return """INSERT INTO %s (%s) VALUES (%s);""" % (
            self.get_table_name(),
            ", ".join(self.attrs.keys()),
            ", ".join("?" for _ in self.attrs),
        )
