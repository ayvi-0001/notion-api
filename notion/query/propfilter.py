import typing

from notion.core import build
from notion.query.conditions import *
from notion.query.filterproto import FilterTypeObject

__all__: typing.Sequence[str] = ['PropertyFilter']


class PropertyFilter(build.NotionObject, FilterTypeObject):
    """ A filter is a single condition used to specify and limit the entries returned from a database query. 
    Database queries can be filtered by page property values. 
    The API supports filtering by the following property types: 
        rich_text, phone_number, number, checkbox, select, multi-select, date, 
        people, files, relation, status, and formula. 
    
    You may also filter a database by created_time or last_edited_time, even if these aren't present as properties on the database. 

    ---
    https://developers.notion.com/reference/post-database-query-filter

    Each database property filter object must contain a property key 
    and a key corresponding with the type of the database property identified by property. 
    The value is an object containing a type-specific filter condition
    https://developers.notion.com/reference/post-database-query-filter#type-specific-filter-conditions
    """
    __slots__: typing.Sequence[str] = (
        '_property_name', 
        '_property_type', 
        '_condition_object', 
        '_object', 
        '_filter'
        )
        
    def __init__(self, property_name: str, filter_condition: FilterConditions, 
                  filter_value: typing.Any, /) -> None:
        super().__init__()

        self._property_type: str
        self._property_name: str = property_name
        self._condition_object = build.NotionObject()
        self._condition_object.set(filter_condition, filter_value)
        self._filter = build.NotionObject()
        self._filter.set('property', self._property_name)
        self._filter.set(self._property_type, self._condition_object)
        self._object = build.NotionObject()
        self._object.set('property', property_name)
        self._object.set(self._property_type, self._condition_object)
        self.set('filter', self._object)


    # @classmethod # TODO
    # def rollup(...)

    @classmethod
    def text(cls, property_name: str, property_type: TextTypes, filter_condition: TextConditions, 
                  filter_value: typing.Any, /):
        cls._property_type = property_type
        return cls(property_name, filter_condition, filter_value)

    @classmethod
    def checkbox(cls, property_name: str, filter_condition: CheckboxConditions, 
                      filter_value: typing.Any, /):
        cls._property_type = 'checkbox'
        return cls(property_name, filter_condition, filter_value)
 
    @classmethod
    def number(cls, property_name: str, filter_condition: NumberConditions, 
                    filter_value: typing.Any, /):
        cls._property_type = 'number'
        return cls(property_name, filter_condition, filter_value)

    @classmethod
    def select(cls, property_name: str, filter_condition: SelectConditions, 
                    filter_value: typing.Any, /):
        cls._property_type = 'select'
        return cls(property_name, filter_condition, filter_value)

    @classmethod
    def multi_select(cls, property_name: str, filter_condition: MultiSelectConditions, 
                          filter_value: typing.Any, /):
        cls._property_type = 'multi_select'
        return cls(property_name, filter_condition, filter_value)

    @classmethod
    def status(cls, property_name: str, filter_condition: StatusConditions, 
                    filter_value: typing.Any, /):
        cls._property_type = 'status'
        return cls(property_name, filter_condition, filter_value)

    @classmethod
    def date(cls, property_name: str, property_type: DateTypes, filter_condition: DateConditions, 
                  filter_value: typing.Any, /):
        """When selecting any DateCondition containing `past`, `this`, or `next`, set filter value to `{}`"""
        cls._property_type = property_type
        return cls(property_name, filter_condition, filter_value)

    @classmethod
    def people(cls, property_name: str, property_type: PeopleTypes, filter_condition: PeopleConditions, 
                   filter_value: typing.Any, /):
        cls._property_type = property_type
        return cls(property_name, filter_condition, filter_value)

    @classmethod
    def files(cls, property_name: str, filter_condition: FilesConditions, 
                   filter_value: typing.Any, /):
        cls._property_type = 'files'
        return cls(property_name, filter_condition, filter_value)

    @classmethod
    def relation(cls, property_name: str, filter_condition: RelationConditions, 
                      filter_value: typing.Any, /):
        cls._property_type = 'relation'
        return cls(property_name, filter_condition, filter_value)
