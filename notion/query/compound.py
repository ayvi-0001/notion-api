from __future__ import annotations
import typing

from notion.core import build
from notion.query.propfilter import PropertyFilter
from notion.query.timestamp import TimestampFilter

__all__: typing.Sequence[str] = ['CompoundFilter']


class CompoundFilter(build.NotionObject):
    """ NOTE: only up to two nesting levels deep.

    :method __and__(): combine all filters in an `and` grouping.
    :method __or__(): combine all filters in an `or` grouping.

    Create a separate CompoundFilter object to nest an `and` operator inside another `and` or `or`.
    
    ---
    https://developers.notion.com/reference/post-database-query-filter#compound-filter-object
    """
    __slots__: typing.Sequence[str] = ()

    def __init__(self) -> None:
        super().__init__()
    
    def __and__(
        self, *filters: PropertyFilter | CompoundFilter | TimestampFilter
    ) -> None:
        filters_ = [f['filter'] if 'filter' in f.keys() else f for f in filters]
        self.nest('filter', 'and', filters_)

    def __or__(
        self, *filters: PropertyFilter | CompoundFilter | TimestampFilter
    ) -> None:
        filters_ = [f['filter'] if 'filter' in f.keys() else f for f in filters]
        self.nest('filter', 'or', filters_)
