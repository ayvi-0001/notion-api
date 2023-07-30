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

from typing import Sequence

from notion.properties.build import NotionObject

__all__: Sequence[str] = ("SortFilter", "PropertyValueSort", "EntryTimestampSort")


class SortFilter(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self, sort_object: Sequence[PropertyValueSort | EntryTimestampSort]
    ) -> None:
        """
        A database query can be sorted by a property and/or timestamp and in a given direction.
        Database queries can also be sorted by two or more properties.

        :param sort_object: (required) A list containing PropertyValueSort/EntryTimestampSort\
                             The sort object listed first in the nested sort list takes precedence.

        https://developers.notion.com/reference/post-database-query-sort#sort-object
        """
        super().__init__()
        self.set("sorts", sort_object)


class PropertyValueSort(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, property_name: str, /, *, direction: str) -> None:
        """This sort orders the database query by a particular property.

        Use one of the following classmethods:
        - `ascending`
        - `descending`

        https://developers.notion.com/reference/post-database-query-sort#property-value-sort
        """
        super().__init__()
        self.set("property", property_name)
        self.set("direction", direction)

    @classmethod
    def ascending(cls, property_name: str) -> PropertyValueSort:
        return cls(property_name, direction="ascending")

    @classmethod
    def descending(cls, property_name: str) -> PropertyValueSort:
        return cls(property_name, direction="descending")


class EntryTimestampSort(NotionObject):
    __slots__: Sequence[str] = ("timestamp", "direction")

    def __init__(self, *, timestamp: str, direction: str) -> None:
        """This sort orders the database query by the timestamp associated with a database entry.

        Use one of the following classmethods:
        - `created_time_ascending`
        - `created_time_descending`
        - `last_edited_time_ascending`
        - `last_edited_time_descending`

        https://developers.notion.com/reference/post-database-query-sort#entry-timestamp-sort
        """
        super().__init__()
        self.timestamp: str = timestamp
        self.direction: str = direction
        self.set("timestamp", self.timestamp)
        self.set("direction", self.direction)

    @classmethod
    def created_time_ascending(cls) -> EntryTimestampSort:
        return cls(timestamp="created_time", direction="ascending")

    @classmethod
    def created_time_descending(cls) -> EntryTimestampSort:
        return cls(timestamp="created_time", direction="descending")

    @classmethod
    def last_edited_time_ascending(cls) -> EntryTimestampSort:
        return cls(timestamp="last_edited_time", direction="ascending")

    @classmethod
    def last_edited_time_descending(cls) -> EntryTimestampSort:
        return cls(timestamp="last_edited_time", direction="descending")
