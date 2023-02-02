from __future__ import annotations
import typing

from notion.core import build
from notion.query.conditions import *
from notion.query.filterproto import FilterTypeObject

__all__: typing.Sequence[str] = ('SortFilter', 'PropertyValueSort', 'EntryTimestampSort')


class SortFilter(build.NotionObject, FilterTypeObject):
    """ A sort is a condition used to order the entries returned from a database query.
    A database query can be sorted by a property and/or timestamp and in a given direction. 
    For example, a library database can be sorted by the "Name of a book" (i.e. property) and in ascending (i.e. direction).
    
    Database queries can also be sorted by two or more properties, which is formally called a nested sort. 
    The sort object listed first in the nested sort list takes precedence.
    
    Required:
    :param sort_object: List containing one of `notion.query.PropertyValueSort` or `notion.query.EntryTimestampSort`

    ---
    https://developers.notion.com/reference/post-database-query-sort#sort-object """
    __slots__: typing.Sequence[str] = ()

    def __init__(self, sort_object: list[PropertyValueSort | EntryTimestampSort]) -> None:
        super().__init__()

        self.set('sorts', sort_object)


class PropertyValueSort(build.NotionObject, FilterTypeObject):
    """ This sort orders the database query by a particular property.
    https://developers.notion.com/reference/post-database-query-sort#sort-object 
    """
    __slots__: typing.Sequence[str] = ()

    def __init__(self, property: str, /, 
                 *, 
                 ascending: bool | None = None, 
                 descending: bool | None = None) -> None:
        super().__init__()

        self.set('property', property)
        self.set('direction', 'ascending') if ascending else None
        self.set('direction', 'descending') if descending else None


class EntryTimestampSort(build.NotionObject, FilterTypeObject):
    """ This sort orders the database query by the timestamp associated with a database entry.
    
    Required:
    - must use either `created_time_ascending` or `created_time_descending` classmethod.
    - must use either `last_edited_time_ascending` or `last_edited_time_descending` classmethod.
    ---
    https://developers.notion.com/reference/post-database-query-sort#entry-timestamp-sort 
    """
    __slots__: typing.Sequence[str] = ('_timestamp', '_direction')

    def __init__(self) -> None:
        super().__init__()

        self._timestamp: str
        self._direction: str
        self.set('timestamp', self._timestamp)
        self.set('direction', self._direction)

    @classmethod
    def created_time_ascending(cls):
        cls._timestamp = 'created_time'
        cls._direction = 'ascending'
        return cls()

    @classmethod
    def created_time_descending(cls):
        cls._timestamp = 'created_time'
        cls._direction = 'descending'
        return cls()

    @classmethod
    def last_edited_time_ascending(cls):
        cls._timestamp = 'last_edited_time'
        cls._direction = 'ascending'
        return cls()

    @classmethod
    def last_edited_time_descending(cls):
        cls._timestamp = 'last_edited_time'
        cls._direction = 'descending'
        return cls()
