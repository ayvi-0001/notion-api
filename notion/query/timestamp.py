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

from typing import Any, MutableMapping, Optional, Sequence, Union

from notion.properties.build import NotionObject
from notion.query.conditions import DateConditions

__all__: Sequence[str] = ["TimestampFilter"]


class TimestampFilter(NotionObject):
    __slots__: Sequence[str] = ["_type"]

    def __init__(
        self,
        filter_condition: DateConditions,
        filter_value: Union[str, MutableMapping[str, Any]],
        /,
        *,
        _type: Optional[str] = None,
    ) -> None:
        """
        A timestamp filter object must contain a timestamp key corresponding to the type of timestamp
        and a key matching that timestamp type which contains a date filter condition.
        Possible values are: "created_time", "last_edited_time".

        Use classmethods:
         - created_time
         - last_edited_time

        https://developers.notion.com/reference/post-database-query-filter#timestamp-filter-object
        """
        super().__init__()
        self.nest("filter", "timestamp", _type)
        self.nest("filter", _type, {filter_condition: filter_value})

    @classmethod
    def created_time(
        cls,
        filter_condition: DateConditions,
        filter_value: Union[str, MutableMapping[str, Any]],
        /,
        *,
        _type: Optional[str] = None,
    ) -> TimestampFilter:
        """
        :param filter_condition: One of the available DateConditions. Must be a string (ISO 8601 date).\
                                 For the following date conditions, the filter_value must be '{}':\
                                 [past_week, past_month, past_year, this_week, next_week, next_month, next_year]

        :param filter_value: Value to filter for.\
                             If a date is provided, the comparison is done against the start and end of the date.\
                             If a date with a time is provided, the comparison is done with millisecond precision.\

        https://developers.notion.com/reference/post-database-query-filter#timestamp-filter-object
        """
        return cls(filter_condition, filter_value, _type="created_time")

    @classmethod
    def last_edited_time(
        cls,
        filter_condition: DateConditions,
        filter_value: Union[str, MutableMapping[str, Any]],
        /,
        *,
        _type: Optional[str] = None,
    ) -> TimestampFilter:
        """
        :param filter_condition: One of the available DateConditions. Must be a string (ISO 8601 date).\
                                 For the following date conditions, the filter_value must be '{}':\
                                 [past_week, past_month, past_year, this_week, next_week, next_month, next_year]

        :param filter_value: Value to filter for.\
                             If a date is provided, the comparison is done against the start and end of the date.\
                             If a date with a time is provided, the comparison is done with millisecond precision.\

        https://developers.notion.com/reference/post-database-query-filter#timestamp-filter-object
        """
        return cls(filter_condition, filter_value, _type="last_edited_time")
