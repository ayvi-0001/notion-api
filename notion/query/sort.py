# MIT License

# Copyright (c) 2023 ayvi-0001

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations

from typing import Optional, Sequence, Union

from notion.properties.build import NotionObject

__all__: Sequence[str] = ("SortFilter", "PropertyValueSort", "EntryTimestampSort")


class SortFilter(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self, sort_object: list[Union[PropertyValueSort, EntryTimestampSort]]
    ) -> None:
        """
        A sort is a condition used to order the entries returned from a database query.
        A database query can be sorted by a property and/or timestamp and in a given direction.
        For example,
        a library database can be sorted by the "Name of a book" (i.e. property) and in ascending (i.e. direction).

        Database queries can also be sorted by two or more properties, which is formally called a nested sort.
        The sort object listed first in the nested sort list takes precedence.

        :param sort_object: (required) List containing one of\
            `notion.query.sort.PropertyValueSort` or `notion.query.sort.EntryTimestampSort`

        https://developers.notion.com/reference/post-database-query-sort#sort-object
        """
        super().__init__()
        self.set("sorts", sort_object)


class PropertyValueSort(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self, property_name: str, /, *, direction: Optional[str] = None
    ) -> None:
        """
        This sort orders the database query by a particular property.
        https://developers.notion.com/reference/post-database-query-sort#sort-object
        """
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


class EntryTimestampSort(NotionObject):
    __slots__: Sequence[str] = ("_timestamp", "_direction")

    def __init__(self) -> None:
        """
        This sort orders the database query by the timestamp associated with a database entry.

        Required:
        - must use either `created_time_ascending` or `created_time_descending` classmethod.
        - must use either `last_edited_time_ascending` or `last_edited_time_descending` classmethod.

        https://developers.notion.com/reference/post-database-query-sort#entry-timestamp-sort
        """
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
