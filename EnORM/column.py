"""Contains column-like classes."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Type

from .exceptions import IncompatibleArgument, OrphanColumn
from .fkey import ForeignKey
from .types import Serial, String


class BaseColumn:
    """Base class for representing a column-like value in a database."""

    aggs: List[str] = []

    def __init__(self) -> None:
        self.alias = None

    def binary_ops(self, other: Any, operator: str) -> str:
        """String representation for direct Python binary operations between :class:`column.BaseColumn` objects.

        E.g.::

            Order.price <= 200.00

        or

            u = User(fullname="Abigail Smith", age=30)

            User.age > u.age

        Has the following:

        :param other:       a literal or a :class:`column.BaseColumn` object, to compare with this object
        :param operator:    SQL operator, represented as a string.
        """
        other_compound = "%s.%s" % (other.view_name, other.variable_name) if isinstance(other, BaseColumn) else other
        full_field_name = ".".join(self.compound_variable_name.split(", "))
        return "%s %s %s" % (full_field_name, operator, other_compound)

    def __eq__(self, other: Any) -> str:
        return self.binary_ops(other, "=")

    def __ne__(self, other: Any) -> str:
        return self.binary_ops(other, "<>")

    def __lt__(self, other: Any) -> str:
        return self.binary_ops(other, "<")

    def __gt__(self, other: Any) -> str:
        return self.binary_ops(other, ">")

    def __le__(self, other: Any) -> str:
        return self.binary_ops(other, "<=")

    def __ge__(self, other: Any) -> str:
        return self.binary_ops(other, ">=")

    def like(self, other: str) -> str:
        return self.binary_ops(other, "LIKE")

    def in_(self, flat_list: Iterable[Any]) -> str:
        flat_list_str = "(%s)" % flat_list
        return self.binary_ops(flat_list_str, "IN")

    def not_in(self, flat_list: Iterable[Any]) -> str:
        flat_list_str = "(%s)" % flat_list
        return self.binary_ops(flat_list_str, "NOT IN")

    def label(self, alias: str) -> BaseColumn:
        """Returns the ORM representation for SQL column aliasing.

        :param alias:   alias as a string.
        """
        self.alias = alias
        return self


class Scalar(BaseColumn):
    """Scalar value as a column.

    :param repr_:   SQL representation of the scalar name.
    """

    def __init__(self, repr_) -> None:
        super(Scalar, self).__init__()
        self.compound_variable_name = repr_


class Field(BaseColumn):
    """Representer of all real and virtual fields."""

    @property
    def compound_variable_name(self):
        return "%s, %s" % (self.view_name, self.variable_name)


class Column(Field):
    """Abstraction of a real table column in a database.

    :param type_:       type of value that this column expects
    :param length:      max length of the expected value. Only works with :class:`.types.String`. Optional
    :param rel:         marker of a relationship -- a foreign key. Optional
    :param primary_key: keyword-only. Whether or not the column is a primary key. Optional
    :param default:     keyword-only. Default value for cells of the column to take. Optional
    :param nullable:    keyword-only. Whether or not the cells of the column are nullable. Optional.

    NOTE that :param type_: must be any of the custom types defined in :module:`.types`.
    """

    objects: Dict[int, Dict[str, Any]] = {}

    def __init__(
        self,
        type_: Type,
        length: Optional[int] = None,
        rel: Optional[ForeignKey] = None,
        *,
        primary_key: bool = False,
        default: Any = None,
        nullable: bool = True,
    ) -> None:
        super(Column, self).__init__()
        self.type = type_
        self.length = length
        self.rel = rel
        self.primary_key = primary_key
        self.default = default
        self.nullable = nullable
        if self.primary_key and self.type not in [Serial, String]:
            raise IncompatibleArgument("Wrong type for primary key.")

        if self.rel is not None:
            if not isinstance(self.rel, ForeignKey):
                raise IncompatibleArgument("Relationship should be a `ForeignKey`.")

            if self.primary_key or self.default or not self.nullable:
                raise IncompatibleArgument("Wrong combination of arguments with `ForeignKey`.")

            if self.type not in [Serial, String]:
                raise IncompatibleArgument("Wrong type for `ForeignKey`.")

        if self.length is not None:
            if self.type != String:
                raise IncompatibleArgument("Only `String` type can have length.")

            if not isinstance(self.length, int):
                raise IncompatibleArgument("`String` type should have an integer length.")

    @property
    def model(self) -> Type:
        """Relational model that the column belongs to."""
        try:
            m = self.objects[id(self)]["model"]
        except KeyError:
            raise OrphanColumn
        return m

    @property
    def variable_name(self) -> str:
        """Name with which the column is defined."""
        try:
            v = self.objects[id(self)]["variable_name"]
        except KeyError:
            raise OrphanColumn
        return v

    @property
    def view_name(self) -> str:
        """Name of the SQL table that the column belongs to."""
        return self.model.get_table_name()


class VirtualField(Field):
    """Abstraction of a virtual table column in a database.

    Never instantiated directly but is derived from actual columns, e.g. by accessing a field of a
    :class:`.query.Subquery` object.

    :param variable_name:   name, as a string, of the column as it is defined in the source
    :param view_name:       name of the view in which the column belongs.
    """

    def __init__(self, variable_name: str, view_name: str) -> None:
        super(VirtualField, self).__init__()
        self.variable_name = variable_name
        self.view_name = view_name
