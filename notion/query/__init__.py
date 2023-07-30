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

""" 
https://developers.notion.com/reference/post-database-query 

notion.query.PropertyFilter && notion.query.TimestampFilter for individual filters as used in Notion UI.

notion.query.CompoundFilter to combine filters.
    :method: _and(): combine all filters in an and grouping.
    :method: _or(): combine all filters in an or grouping.

    Create a separate CompoundFilter object to nest an and/or operator inside another and/or.

notion.query.SortFilter takes a list of either *notion.query.PropertyValueSort | notion.query.EntryTimestampSort
"""
from typing import Sequence

from notion.query.compound import CompoundFilter
from notion.query.propfilter import PropertyFilter
from notion.query.sort import EntryTimestampSort, PropertyValueSort, SortFilter
from notion.query.timestamp import TimestampFilter

__all__: Sequence[str] = (
    "SortFilter",
    "PropertyFilter",
    "CompoundFilter",
    "TimestampFilter",
    "EntryTimestampSort",
    "PropertyValueSort",
)
