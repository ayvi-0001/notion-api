from __future__ import annotations
from typing import Sequence
from typing import Union

from notion.core import build
from notion.query.propfilter import PropertyFilter
from notion.query.timestamp import TimestampFilter

__all__: Sequence[str] = ['CompoundFilter']


class CompoundFilter(build.NotionObject):
    """ NOTE: only up to two nesting levels deep.

    :method _and_(): combine all filters in an `and` grouping.
    :method _or_(): combine all filters in an `or` grouping.

    Create a separate CompoundFilter object to nest an `and` operator inside another `and` or `or`.
    
    https://developers.notion.com/reference/post-database-query-filter#compound-filter-object
    """
    __slots__: Sequence[str] = ()

    def __init__(self) -> None:
        super().__init__()
    
    def _and_(self, *filters: FilterTypeObjects) -> None:
        filters_ = [f['filter'] if 'filter' in f.keys() else f for f in filters]
        self.nest('filter', 'and', filters_)

    def _or_(self, *filters: FilterTypeObjects) -> None:
        filters_ = [f['filter'] if 'filter' in f.keys() else f for f in filters]
        self.nest('filter', 'or', filters_)


FilterTypeObjects = Union[PropertyFilter, CompoundFilter, TimestampFilter]

