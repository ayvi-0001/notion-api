import typing

from notion.core import build
from notion.query.conditions import *
from notion.query.conditions import DateConditions
from notion.query.filterproto import FilterTypeObject

__all__: typing.Sequence[str] = ['TimestampFilter']


class TimestampFilter(build.NotionObject, FilterTypeObject):
    """ A timestamp filter object must contain a timestamp key corresponding to the type of timestamp 
    and a key matching that timestamp type which contains a date filter condition.
    Possible values are: "created_time", "last_edited_time".

    Required:
    - must use either `created_time` or `last_edited_time` classmethod.

    :param filter_condition: One of the available DateConditions. Must be a string (ISO 8601 date).
                          for the following date conditions, the filter_value must be '{}'
                          [past_week past_month past_year this_week next_week next_month next_year]

    :param filter_value: Value to filter for.
                         If a date is provided, the comparison is done against the start and end of the UTC date.
                         If a date with a time is provided, the comparison is done with millisecond precision.
                         Note that if no timezone is provided, the default is UTC.
    ---
    https://developers.notion.com/reference/post-database-query-filter#timestamp-filter-object
    """
    __slots__: typing.Sequence[str] = ('_filter_condition', '_filter_type')

    def __init__(self, filter_condition: DateConditions, filter_value: str | dict, /) -> None:
        super().__init__()

        self._filter_type: str

        self._filter_condition = build.NotionObject()
        self._filter_condition.set(filter_condition, filter_value)

        self._object = build.NotionObject()
        self._object.set('timestamp', self._filter_type)
        self._object.set(self._filter_type, self._filter_condition)
        self.set('filter', self._object)
        
    @classmethod
    def created_time(cls, filter_condition: DateConditions, filter_value: str | dict, /):
        cls._filter_type = 'created_time'
        return cls(filter_condition, filter_value)

    @classmethod
    def last_edited_time(cls, filter_condition: DateConditions, filter_value: str | dict, /):
        cls._filter_type = 'last_edited_time'
        return cls(filter_condition, filter_value)
