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

""" Type-specific filter conditions
https://developers.notion.com/reference/post-database-query-filter#type-specific-filter-conditionss
"""
from typing import Literal, Sequence, TypeAlias, Union

__all__: Sequence[str] = (
    "TextConditions",
    "TextTypes",
    "NumberConditions",
    "CheckboxConditions",
    "SelectConditions",
    "MultiSelectConditions",
    "StatusConditions",
    "DateConditions",
    "DateTypes",
    "PeopleConditions",
    "PeopleTypes",
    "FilesConditions",
    "RelationConditions",
    "RollupConditions",
    "FormulaConditions",
    "FilterConditions",
)


TextConditions: TypeAlias = Literal[
    "equals",
    "does_not_equal",
    "contains",
    "does_not_contain",
    "starts_with",
    "ends_with",
    "is_empty",
    "is_not_empty",
]

TextTypes: TypeAlias = Literal[
    "title",
    "rich_text",
    "url",
    "email",
]

NumberConditions: TypeAlias = Literal[
    "equals",
    "does_not_equal",
    "greater_than",
    "less_than",
    "greater_than_or_equal_to",
    "less_than_or_equal_to",
    "is_empty",
    "is_not_empty",
]

CheckboxConditions: TypeAlias = Literal["equals", "does_not_equal"]

SelectConditions: TypeAlias = Literal[
    "equals", "does_not_equal", "is_empty", "is_not_empty"
]

MultiSelectConditions: TypeAlias = Literal[
    "contains", "does_not_contain", "is_empty", "is_not_empty"
]

StatusConditions: TypeAlias = Literal[
    "equals", "does_not_equal", "is_empty", "is_not_empty"
]

DateConditions: TypeAlias = Literal[
    "equals",
    "before",
    "after",
    "on_or_before",
    "is_empty",
    "is_not_empty",
    "on_or_after",
    "past_week",
    "past_month",
    "past_year",
    "this_week",
    "next_week",
    "next_month",
    "next_year",
]

DateTypes: TypeAlias = Literal[
    "date",
    "created_time",
    "last_edited_time",
]

PeopleConditions: TypeAlias = Literal[
    "contains", "does_not_contain", "is_empty", "is_not_empty"
]

PeopleTypes: TypeAlias = Literal[
    "people",
    "created_by",
    "last_edited_by",
]

FilesConditions: TypeAlias = Literal["is_empty", "is_not_empty"]

RelationConditions: TypeAlias = Literal[
    "contains", "does_not_contain", "is_empty", "is_not_empty"
]

RollupConditions: TypeAlias = Literal["any", "every", "none", "number", "date"]

FormulaConditions = Union[
    TextConditions, NumberConditions, CheckboxConditions, DateConditions
]

FilterConditions: TypeAlias = Union[
    TextConditions,
    TextTypes,
    NumberConditions,
    CheckboxConditions,
    SelectConditions,
    MultiSelectConditions,
    StatusConditions,
    DateConditions,
    DateTypes,
    PeopleConditions,
    PeopleTypes,
    FilesConditions,
    RelationConditions,
    RollupConditions,
]
