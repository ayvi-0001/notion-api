""" 
Visit https://developers.notion.com/reference/post-database-query for info on database queries and filter/sort objects.

`from notion.query import *`

`notion.query.PropertyFilter` && `notion.query.TimestampFilter` for individual filters as used in Notion UI.

`notion.query.CompoundFilter` to combine filters.
    :method __and__(): combine all filters in an `and` grouping.
    :method __or__(): combine all filters in an `or` grouping.

    Create a separate CompoundFilter object to nest an `and` operator inside another `and` or `or`.

`notion.query.SortFilter` contains a list of either *`notion.query.PropertyValueSort` || `notion.query.EntryTimestampSort`
"""
from notion.query.compound import *
from notion.query.conditions import *
from notion.query.propfilter import *
from notion.query.timestamp import *
from notion.query.sort import *

from typing import Sequence

__all__: Sequence[str] = (
    "SortFilter",
    "PropertyFilter",
    "CompoundFilter", 
    "TimestampFilter",
    "EntryTimestampSort",
    "PropertyValueSort",
)
