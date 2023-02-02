from __future__ import annotations
import typing

from notion.core import build
from notion.query.conditions import *
from notion.query.propfilter import PropertyFilter
from notion.query.filterproto import FilterTypeObject

__all__: typing.Sequence[str] = ('CompoundFilter', 'AndOperator', 'OrOperator')


class CompoundFilter(build.NotionObject, FilterTypeObject):
    """
    Required:
    :param operator: Either `notion.query.AndOperator` or notion.query.OrOperator`. 
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
        for op in operators:
            if isinstance(op, build.NotionObject) or isinstance(op, dict):
                self._all.update(op)
        
        self.set('filter', self._all)


class AndOperator(build.NotionObject, FilterTypeObject):
    __slots__: typing.Sequence[str] = ('_filters')

    def __init__(self, *filters: FilterTypeObject | dict) -> None:
        super().__init__()
        self._filters: list = []
        
        for f in filters:
            if isinstance(f, dict) or isinstance(f, PropertyFilter):
                self._filters.append(f['filter'] if 'filter' in f.keys() else f)

        self.set('and', self._filters)


class OrOperator(build.NotionObject, FilterTypeObject):
    __slots__: typing.Sequence[str] = ('_filters')

    def __init__(self, *filters: FilterTypeObject | dict) -> None:
        super().__init__()
        self._filters: list = []
        
        for f in filters:
            if isinstance(f, dict) or isinstance(f, PropertyFilter):
                self._filters.append(f['filter'] if 'filter' in f.keys() else f)

        self.set('or', self._filters)
