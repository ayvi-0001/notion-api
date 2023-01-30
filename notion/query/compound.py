from __future__ import annotations
import typing

from notion.core import build
from notion.query.conditions import *
from notion.query.propfilter import PropertyFilter
from notion.query.filterproto import FilterTypeObject

__all__: typing.Sequence[str] = ('CompoundFilter', 'AndOperator', 'OrOperator')

_PropertyFilter = typing.Union[PropertyFilter, typing.Sequence[PropertyFilter]]


class CompoundFilter(build.NotionObject, FilterTypeObject):
    """
    :param operator: :class:`AndOperator` or :class:`OrOperator` 
                     array of PropertyFilter objects or CompoundFilter objects.
                     Returns pages when any of the filters inside the provided array match.
    ---
    Combines several filter objects together using a logical operator `and` or `or`.  
    Can also be combined within a compound filter, 
    NOTE: only up to two nesting levels deep.

    ---
    https://developers.notion.com/reference/post-database-query-filter#compound-filter-object
    """
    __slots__: typing.Sequence[str] = ('_all')

    def __init__(self, *operators: AndOperator | OrOperator) -> None:
        super().__init__()

        self._all: dict = {}
        for x in operators:
            if isinstance(x, build.NotionObject) or isinstance(x, dict):
                self._all.update(x)
        
        self.set('filter', self._all)

class AndOperator(build.NotionObject, FilterTypeObject):
    __slots__: typing.Sequence[str] = ()

    def __init__(self, *filters: FilterTypeObject) -> None:
        super().__init__()
        self.set('and', [x for x in filters])


class OrOperator(build.NotionObject, FilterTypeObject):
    __slots__: typing.Sequence[str] = ()

    def __init__(self, *filters: FilterTypeObject) -> None:
        super().__init__()
        self.set('or', [x for x in filters])
