"""Contains :class:`.fkey.ForeignKey`."""

from typing import Optional, Type

from .exceptions import IncompatibleArgument

CASCADE = "cascade"


class ForeignKey:
    """Representer of foreign key relations.

    This class implements logic handling relations across tables through connector columns.

    :param foreign_model:   `MappedClass` that represents a foreign model
    :param reverse_name:    keyword-only. Relation name on the related class tied to this class
    :param on_delete:       keyword-only. Whether to delete cascade style or not. Optional
    :param on_update:       keyword-only. Whether to update cascade style or not. Optional.
    """

    def __init__(
        self,
        foreign_model: Type,
        *,
        reverse_name: str,
        on_delete: Optional[str] = None,
        on_update: Optional[str] = None,
    ) -> None:
        self.foreign_model = foreign_model
        self.reverse_name = reverse_name
        self.on_delete = on_delete
        self.on_update = on_update
        if self.on_delete not in [None, CASCADE]:
            raise IncompatibleArgument("Wrong value for `on_delete`")
        if self.on_update not in [None, CASCADE]:
            raise IncompatibleArgument("Wrong value for `on_update`")
