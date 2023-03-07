from __future__ import annotations
from typing import Union
from typing import Sequence
from typing import Optional

from notion.core import build

__all__: Sequence[str] = ("SortFilter", "PropertyValueSort", "EntryTimestampSort")


class SortFilter(build.NotionObject):
    """ 
    A sort is a condition used to order the entries returned from a database query.
    A database query can be sorted by a property and/or timestamp and in a given direction. 
    For example, 
    a library database can be sorted by the "Name of a book" (i.e. property) and in ascending (i.e. direction).
    
    Database queries can also be sorted by two or more properties, which is formally called a nested sort. 
    The sort object listed first in the nested sort list takes precedence.
    
    :param sort_object: (required) List containing one of \
        `notion.query.sort.PropertyValueSort` or `notion.query.sort.EntryTimestampSort`

    https://developers.notion.com/reference/post-database-query-sort#sort-object """

    __slots__: Sequence[str] = ()

    def __init__(
        self, sort_object: list[Union[PropertyValueSort, EntryTimestampSort]]
    ) -> None:
        super().__init__()
        self.set("sorts", sort_object)


class PropertyValueSort(build.NotionObject):
    """
    This sort orders the database query by a particular property.
    https://developers.notion.com/reference/post-database-query-sort#sort-object
    """

    __slots__: Sequence[str] = ()

    def __init__(
        self, property_name: str, /, *, direction: Optional[str] = None
    ) -> None:
        super().__init__()
        self.set("property", property_name)
        self.set("direction", direction)

    @classmethod
    def ascending(
        cls, property_name: str, /, *, direction: Optional[str] = "ascending"
    ) -> PropertyValueSort:
        return cls(property_name, direction=direction)

    @classmethod
    def descending(
        cls, property_name: str, /, *, direction: Optional[str] = "descending"
    ) -> PropertyValueSort:
        return cls(property_name, direction=direction)


class EntryTimestampSort(build.NotionObject):
    """
    This sort orders the database query by the timestamp associated with a database entry.

    Required:
    - must use either `created_time_ascending` or `created_time_descending` classmethod.
    - must use either `last_edited_time_ascending` or `last_edited_time_descending` classmethod.

    https://developers.notion.com/reference/post-database-query-sort#entry-timestamp-sort
    """

    __slots__: Sequence[str] = ("_timestamp", "_direction")

    def __init__(self) -> None:
        super().__init__()

        self._timestamp: str
        self._direction: str
        self.set("timestamp", self._timestamp)
        self.set("direction", self._direction)

    @classmethod
    def created_time_ascending(cls) -> EntryTimestampSort:
        cls._timestamp = "created_time"
        cls._direction = "ascending"
        return cls()

    @classmethod
    def created_time_descending(cls) -> EntryTimestampSort:
        cls._timestamp = "created_time"
        cls._direction = "descending"
        return cls()

    @classmethod
    def last_edited_time_ascending(cls) -> EntryTimestampSort:
        cls._timestamp = "last_edited_time"
        cls._direction = "ascending"
        return cls()

    @classmethod
    def last_edited_time_descending(cls) -> EntryTimestampSort:
        cls._timestamp = "last_edited_time"
        cls._direction = "descending"
        return cls()
