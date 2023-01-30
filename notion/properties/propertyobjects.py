"""Metadata that controls how a database property behaves. 
Each database property object contain the following; 
 - The ID of the property, usually a short string of random letters and symbols.
   Some automatically generated property types have special human-readable IDs. 
   For example, all Title properties have an ID of "title".name, id, and  key corresponding 
 - The name of the property as it appears in Notion.
 - A key corresponding with the value of type. The value is an object containing 
   type-specific configuration that controls the behavior of the property
---
NOTE: The API doesn't support creating, updating, or deleting rollup database properties.
The following section details how the Notion API returns rollups in a Retrieve database or Query a database request.
Use the Notion UI to create or update a rollup database property.
---
https://developers.notion.com/reference/property-object
"""
import typing

from notion.core import build
from notion.properties.options import PropertyColors
from notion.properties.options import NumberEnum
from notion.core.typedefs import PropertyObject

__all__: typing.Sequence[str] = (
    "RelationPropertyObject",
    "Option",
    "Group",
    "StatusOptions",
    "StatusGroups",
    "MultiSelectPropertObject",
    "SelectPropertObject",
    "StatusPropertyObject",
    "NumberPropertObject",
    "FormulaPropertyObject",
    "CheckboxPropertyObject",
    "PeoplePropertyObject",
    "PhoneNumberPropertyObject",
    "RichTextPropertyObject",
    "CreatedTimePropertyObject",
    "CreatedByPropertyObject",
    "LastEditedTimePropertyObject",
    "LastEditedByPropertyObject",
    "DatePropertyObject",
    "EmailPropertyObject",
    "FilesPropertyObject",
    "TitlePropertyObject",
    "URLPropertyObject",
    # "RollupPropertyObject",
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~       Single/Dual Related Properties       ~~~~~

class _Dual_Property(build.NotionObject, PropertyObject):
    __slots__: typing.Sequence[str] = ('name', '_property')

    def __init__(self, database_id: str, synced_property_name: str, /) -> None:
        super().__init__()

        self._property = build.NotionObject()
        self._property.set('synced_property_name', synced_property_name)

        self.set('database_id', database_id)
        self.set('type', 'dual_property')
        self.set('dual_property', self._property)

class _Single_Property(build.NotionObject, PropertyObject):
    __slots__: typing.Sequence[str] = ()

    def __init__(self, database_id: str, /) -> None:
        super().__init__()

        self.set('database_id', database_id)
        self.set('type', 'single_property')
        self.set('single_property', {})

class RelationPropertyObject(build.NotionObject, PropertyObject):
    """Use either classmethod: `dual`/`single`
    https://developers.notion.com/reference/property-object#relation
    """
    __slots__: typing.Sequence[str] = ('name', '_related_to_')

    def __init__(self, *, database_id: str, synced_property_name: str | None = None, 
                 property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self._related_to_: build.NotionObject | _Dual_Property | _Single_Property

        self.set('type', 'relation')
        self.set('relation', self._related_to_)


    @classmethod
    def dual(cls, database_id: str, synced_property_name: str, /, *, property_name: str | None = None):
        """
        (required)
        :param database_id: The database that the relation property refers to.
                            The corresponding linked page values must belong to the database in order to be valid.
        :param synced_property_name: The id of the corresponding property that is updated in the related database when this property is changed.
        :param synced_property_name: The name of the corresponding property that is updated in the related database when this property is changed.
        """
        cls._related_to_ = _Dual_Property(database_id, synced_property_name)
        return cls(database_id=database_id,
                   synced_property_name=synced_property_name, 
                   property_name=property_name)
        
    @classmethod
    def single(cls, database_id: str, /, *, property_name: str | None = None):
        """
        (required)
        :param database_id: The database that the relation property refers to.
                            The corresponding linked page values must belong to the database in order to be valid.
        """
        cls._related_to_ = _Single_Property(database_id)
        return cls(database_id=database_id, 
                   property_name=property_name)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~ Select/Multi Select/Status: Options/Groups ~~~~~

class Option(build.NotionObject, PropertyObject):
    """
    (required)
    :param name: The name of the option as it appears in the Notion UI.
                 Note: Commas (",") are not valid for select values.
    :param color: The color of the option as rendered in the Notion UI.
                  Use `notion.properties.PropertyColor` for reference.
    """
    __slots__: typing.Sequence[str] = ()

    def __init__(self, option_name: str, color: PropertyColors | str, /) -> None:
        super().__init__()

        self.set('name', option_name)
        self.set('color', color)

class Group(build.NotionObject, PropertyObject):
    """
    (required)
    :param name: The name of the option as it appears in the Notion UI.
                 Note: Commas (",") are not valid for select values.
    :param color: The color of the option as rendered in the Notion UI.
                  Use `notion.properties.PropertyColor` for reference.
    """
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, group_name: str, color: PropertyColors | str, /) -> None:
        super().__init__()

        self.set('name', group_name)
        self.set('color', color)

class StatusOptions(build.NotionObject, PropertyObject):
    """This class is only used when describing the database schema for a Status-type property,
    which requires the key `options` before the array of individual options. The page property value
    endpoint does not require this key.
    """
    __slots__: typing.Sequence[str] = ()
   
    def __init__(self, *options: Option) -> None:
        super().__init__()
        self.set('options', options)

class StatusGroups(build.NotionObject, PropertyObject):
    """This class is only used when describing the database schema for a Status-type property,
    which requires the key `groups` before the array of individual groups. The page property value
    endpoint does not require this key.
    """
    __slots__: typing.Sequence[str] = ()

    def __init__(self, *groups: Group) -> None:
        super().__init__()
        self.set('groups', groups)

# ~~~~~                                            ~~~~~

class MultiSelectPropertObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#multi-select"""
    __slots__: typing.Sequence[str] = ('name', '_options')

    def __init__(self, *options: Option, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self._options = build.NotionObject()
        self._options.set('options', options)

        self.set('type', 'multi_select')
        self.set('multi_select', self._options)


class SelectPropertObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#select"""
    __slots__: typing.Sequence[str] = ('name', '_options')

    def __init__(self, *options: Option, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self._options = build.NotionObject()
        self._options.set('options', options)

        self.set('type', 'select')
        self.set('select', self._options)


class StatusPropertyObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#status"""
    __slots__: typing.Sequence[str] = ('name', '_config')
    
    def __init__(self, /, *, 
                 groups: tuple[Group, ...], 
                 options: tuple[Option, ...], 
                 property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self._config = build.NotionObject()
        self._config.set('groups', groups)
        self._config.set('options', options)

        self.set('type', 'select')
        self.set('status', self._config)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NumberPropertObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#number"""
    __slots__: typing.Sequence[str] = ('name', '_format')
    
    def __init__(self, format: NumberEnum, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self._format = build.NotionObject()
        self._format.set('format', format)

        self.set('type', 'number')
        self.set('number', self._format)


class FormulaPropertyObject(build.NotionObject, PropertyObject):
    """
    (required)
    :param expression: The formula that is used to compute the values for this property.
                       Refer to the Notion help center for information about formula syntax.
    ---
    https://developers.notion.com/reference/property-object#formula
    """
    __slots__: typing.Sequence[str] = ('name', '_formula')
    
    def __init__(self, expression: str, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self._formula = build.NotionObject()
        self._formula.set('expression', expression)

        self.set('type', 'formula')
        self.set('formula', self._formula)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~   Property Objects - No Additional Config  ~~~~~

class CheckboxPropertyObject(build.NotionObject, PropertyObject):
    __slots__: typing.Sequence[str] = ('name')

    def __init__(self, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'checkbox')
        self.set('checkbox', {})
        

class PeoplePropertyObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#people"""
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'people')
        self.set('people', {})


class PhoneNumberPropertyObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#phone-number"""
    __slots__: typing.Sequence[str] = ('name')

    def __init__(self, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'phone_number')
        self.set('phone_number', {})


class RichTextPropertyObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#rich-text"""
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'rich_text')
        self.set('rich_text', {})


class CreatedTimePropertyObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#created-time"""
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'created_time')
        self.set('created_time', {})
        

class CreatedByPropertyObject(build.NotionObject, PropertyObject):
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'created_by')
        self.set('created_by', {})
        

class LastEditedTimePropertyObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#last-edited-by"""
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'last_edited_time')
        self.set('last_edited_time', {})
        

class LastEditedByPropertyObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#last-edited-time"""
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'last_edited_by')
        self.set('last_edited_by', {})
        
  
class DatePropertyObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#date"""
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'date')
        self.set('date', {})
        

class EmailPropertyObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#email"""
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'email')
        self.set('email', {})
        

class FilesPropertyObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#files"""
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'files')
        self.set('files', {})
        

class TitlePropertyObject(build.NotionObject, PropertyObject):
    """A title database property controls the title that appears at the top of a page when a 
    database row is opened. The title type object itself is empty; there is no additional configuration.

    NOTE: All databases require one, and only one, title property.
          The API throws errors if you send a request to Create a database without a title property, 
          or if you attempt to Update a database to add or remove a title property.
    ---
    ### Title database property vs. database title
    A title database property is a type of column in a database.
    A database title defines the title of the database and is found on the database object.
    Every database requires both a database title and a title database property.
    ---
    https://developers.notion.com/reference/property-object#title
    """
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, property_name: str, /) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'title')
        self.set('title', {})


class URLPropertyObject(build.NotionObject, PropertyObject):
    """https://developers.notion.com/reference/property-object#url"""
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'url')
        self.set('url', {})


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# from ... import FunctionsEnum

# class RollupPropertyObject(build.NotionObject, PropertyObject):
#     """https://developers.notion.com/reference/property-object#rollup"""
#     def __init__(self, relation_property_name: str, rollup_property_name: str, 
#                  function: FunctionsEnum | str, /, *, property_name: str | None = None) -> None:
#         super().__init__()

#         self._config = build.NotionObject()
#         self._config.set('relation_property_name', relation_property_name)
#         self._config.set('rollup_property_name', rollup_property_name)
#         self._config.set('function', function)

#         self.set('type', 'rollup')
#         self.set('rollup', self._config)

#         if property_name:
#             self.name = property_name
#             self.set('name', self.name)

