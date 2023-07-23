from __future__ import annotations

from typing import Any, Dict, List, Optional, Type

from .column import Column, Label
from .exceptions import FieldNotExist, MissingRequiredField, WrongFieldType
from .query import Query
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

    __dep_mapping: Dict[type, List[type]] = {}

    model_definition_sqls: List[str] = []

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        fields = cls.get_fields()
        tablename = cls.get_table_name()
        def_sql = """DROP TABLE %s IF EXISTS; CREATE TABLE %s (%s);""" % (
            tablename,
            tablename,
            ", ".join(cls.get_type_pref(field, val) for field, val in fields.items()),
        )
        cls.model_definition_sqls.append(def_sql)

        for field, val in fields.items():
            Column.objects[id(val)] = {"model": cls, "variable_name": field}
            if val.rel is not None:
                cls.__dep_mapping[val.rel.foreign_model] = [*cls.__dep_mapping.get(val.rel.foreign_model, []), cls]

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
        return cls.__table__ or "%ss" % cls.__qualname__.split(".")[-1].lower()

    @classmethod
    def get_primary_key_column(cls) -> Optional[Column]:
        return next((c for _, c in cls.get_fields().items() if c.primary_key), None)

    @classmethod
    def get_connector_column(cls, mapped: Type) -> Optional[Column]:
        return next(
            (c for _, c in cls.get_fields().items() if c.rel is not None and c.rel.foreign_model == mapped),
            None,
        )

    @classmethod
    def get_type_pref(cls, field: str, val: Column) -> str:
        type_pref_inc = cls.__TYPES[val.type]
        if val.rel is not None:
            pref = "%s %s FOREIGN KEY (%s) REFERENCES %s(%s)" % (
                field,
                type_pref_inc,
                field,
                val.rel.foreign_model.get_table_name(),
                val.rel.foreign_model.get_primary_key_column().variable_name,
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

    def __getattr__(self, attr: str) -> Any:
        self_model = type(self)
        try:
            fields = self_model.get_fields()
            return fields[attr]
        except KeyError as e:
            for m in self_model.__dep_mapping[self_model]:
                connector = m.get_connector_column(self_model)
                if connector.rel.reverse_name == attr:
                    return Query(m).join(self_model).subquery()

            raise FieldNotExist(attr) from e

    @property
    def sql(self) -> str:
        return """INSERT INTO %s (%s) VALUES (%s);""" % (
            self.get_table_name(),
            ", ".join(self.attrs.keys()),
            ", ".join("?" for _ in self.attrs),
        )
