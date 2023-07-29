"""Contains :class:`.fkey.ForeignKey`."""

from typing import Optional, Type

from .exceptions import IncompatibleArgument

CASCADE = "cascade"


class ForeignKey:
    """Docstring here."""

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
