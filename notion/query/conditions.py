""" Type-specific filter conditions
https://developers.notion.com/reference/post-database-query-filter#type-specific-filter-conditionss
"""
from __future__ import annotations
from typing import Sequence
from typing import Union
from typing import Literal
from typing import TypeAlias

__all__: Sequence[str   ] = (
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
    'equals',
    'does_not_equal',
    'contains',
    'does_not_contain',
    'starts_with',
    'ends_with',
    'is_empty',
    'is_not_empty'
    ]

TextTypes: TypeAlias = Literal[
    'title',
    'rich_text',
    'url',
    'email',
    ]

NumberConditions: TypeAlias = Literal[
    'equals',
    'does_not_equal',
    'greater_than',
    'less_than',
    'greater_than_or_equal_to',
    'less_than_or_equal_to',
    'is_empty',
    'is_not_empty'
    ]

CheckboxConditions: TypeAlias = Literal[
    'equals',
    'does_not_equal'
    ]

SelectConditions: TypeAlias = Literal[
    'equals',
    'does_not_equal',
    'is_empty',
    'is_not_empty'
    ]

MultiSelectConditions: TypeAlias = Literal[
    'contains',
    'does_not_contain',
    'is_empty',
    'is_not_empty'
    ]

StatusConditions: TypeAlias = Literal[
    'equals',
    'does_not_equal',
    'is_empty',
    'is_not_empty'
    ]

DateConditions: TypeAlias = Literal[
    'equals',
    'before',
    'after',
    'on_or_before',
    'is_empty',
    'is_not_empty',
    'on_or_after',
    'past_week',
    'past_month',
    'past_year',
    'this_week',
    'next_week',
    'next_month',
    'next_year'
    ]

DateTypes: TypeAlias = Literal[
    'date',
    'created_time',
    'last_edited_time',
    ]

PeopleConditions: TypeAlias = Literal[
    'contains',
    'does_not_contain',
    'is_empty',
    'is_not_empty'
    ]

PeopleTypes: TypeAlias = Literal[
    'people',
    'created_by',
    'last_edited_by',
    ]

FilesConditions: TypeAlias = Literal[
    'is_empty',
    'is_not_empty'
    ]

RelationConditions: TypeAlias = Literal[
    'contains',
    'does_not_contain',
    'is_empty',
    'is_not_empty'
    ]

RollupConditions: TypeAlias = Literal[
    'any', 
    'every', 
    'none', 
    'number', 
    'date'
    ]

FormulaConditions = Union[TextConditions, NumberConditions, CheckboxConditions, DateConditions  ]

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