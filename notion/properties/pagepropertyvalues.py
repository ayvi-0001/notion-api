"""
The endpoint limits the page response object to 25 references across all page properties. 
If a page object's Parent object is a database, then the property values conform to the database property schema. 
If a page object is not part of a database, then the only property value available for that page is its title.
The Retrieve a page property item endpoint returns information for a single property.

2 types of responses: 
Retrieve a page endpoint response object (named_property), 
Retrieve a page property item endpoint response object (paginated list of results with values) 
---
For information about size limitations for specific page property objects, 
refer to https://developers.notion.com/reference/request-limits#limits-for-property-values
---

NOTE: The following property values cannot be updated directly via the API and are excluded.
- Created By
- Created Time
- Last Edited By
- Last Edited Time
- Rollup results *function can still be updated*
- Formula property value objects represent the result of evaluating a formula described in the
    database's properties. They contain a formula object with a type of either boolean/date/number/string.
    The value can't be updated directly via the API.
---
FilesPropertyValue can be found in `notion.properties.files`.
---
https://developers.notion.com/reference/page-property-values
"""
from __future__ import annotations
import typing
from datetime import datetime

from notion.core import build
from notion.properties.propertyobjects import Option
from notion.properties.options import FunctionsEnum
from notion.properties.richtext import RichText
from notion.properties.user import UserObject
from notion.properties.common import NotionUUID
from notion.core.typedefs import PagePropertyValue

if typing.TYPE_CHECKING:
    from notion.core.typedefs import DateISO8601

__all__: typing.Sequence[str] = (
    "RichTextPropertyValue",
    "TitlePropertyValue",
    "DatePropertyValue",
    "RelationPropertyValue",
    "StatusPropertyValue",
    "SelectPropertyValue",
    "MultiSelectPropertyValue",
    "CheckboxPropertyValue",
    "PeoplePropertyValue",
    "RollupPropertyValue",
    "EmailPropertyValue",
    "NumberPropertyValue",
    "PhoneNumberPropertyValue",
    "URLPropertyValue",
    )


class RichTextPropertyValue(build.NotionObject, PagePropertyValue):
    r"""The purpose of the rich text property value is to provide the key `rich_text`, whereas the object
    `notion.properties.RichText` has the key `text`. 
    ---
    (required)
    :param array_of_rich_text: An array of rich text objects.
    ---
    Using `shift+enter` for multi-line text blocks results in 
    a separate `text` key with a newline escape. E.g.

    ```json
    },  // ... first text line above
    {
        "type": "text",
        "text": {
            "content": "\nthis is the second line of a block"
        }
    }   
    ```
    ---
    If you hyperlink only part of a string in Notion, the string will be split and return
    as separate keys in the rich text object.
    ---
    Hyperlinking text to an internal Notion link will populate link/href
    with the UUID's following notion.so/{workspace name}/...

    ```json
    {
        "type": "text",
        "text": {
            "content": "hyperlink in text to notion link\n",
            "link": {
                "url": "/3a2ec1e9308b4fd5a5749a5ee5aeeff9?v=f19121cb8e6f4329aba62edef93c39dc&p=bc5d3abdf3a942e0b6a7d8a5c94b5dc9&pm=s"
            }          // database id // database view id // database page id
    },
    ```
    ---
    :The RichText Object: https://developers.notion.com/reference/rich-text
    :The RichText Property Value: https://developers.notion.com/reference/page-property-values#rich-text
    """
    __slots__: typing.Sequence[str] = ('name')

    def __init__(self, array_of_rich_text: list[RichText], /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'rich_text')
        self.set('rich_text', array_of_rich_text)


class TitlePropertyValue(build.NotionObject, PagePropertyValue):
    """
    (required)
    :param title: An array of rich text objects: `notion.properties.RichText`
    --- 
    https://developers.notion.com/reference/page-property-values#title
    """
    __slots__: typing.Sequence[str] = ('name')

    def __init__(self, title: list[RichText], /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'title')
        self.setdefault('title', [])
        self.set('title', title)


class DatePropertyValue(build.NotionObject, PagePropertyValue):
    """Notion uses ISO 8601 date and time for some endpoints, and YYYY/MM/DD for others.
    If a datetime object is passed to either parameter, they'll be converted to isoformat.
    ---
    (required)
    :param start: A date, with an optional time. If the "date" value is a range, then start represents the start of the range.
    ---
    (optional)
    :param end: A string representing the end of a date range. If the value is null, then the date value is not a range. 
    
    ---
    https://developers.notion.com/reference/page-property-values#date
    """
    __slots__: typing.Sequence[str] = ('name', '_date')
    
    def __init__(self, start: str | datetime, end: str | DateISO8601 | None = None, 
                 /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        if isinstance(start, datetime):
            start = start.isoformat()
        if isinstance(end, datetime):
            end = end.isoformat()

        self._date = build.NotionObject()
        self._date.set('start', start)
        self._date.set('end', end)
        self.set('date', self._date)


class RelationPropertyValue(build.NotionObject, PagePropertyValue):
    """NOTE: updating a relation property value with an empty array will clear the list.
    (required)
    :param related_ids: An array of related page references. 
                        A page reference is an object with an id key and a string value (UUIDv4) 
                        corresponding to a page ID in another database.

    :param has_more: If a relation has more than 25 references, then the has_more value for 
                     the relation in the response object is true. If a relation doesn't 
                     exceed the limit, then has_more is false.
    ---
    https://developers.notion.com/reference/page-property-values#relation
    """
    __slots__: typing.Sequence[str] = ('name')

    def __init__(self, *related_ids: list[NotionUUID], property_name: str | None = None, has_more: bool | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'relation')
        self.setdefault('relation', [])
        self.set('relation', related_ids)
        self.setdefault('has_more', False)
        if has_more:
            self.set('has_more', True)


class StatusPropertyValue(build.NotionObject, PagePropertyValue):
    """
    (required)
    :param status_option: a single status option: `notion.properties.Option` 
                             containing `name` and `notion.properties.PropertyColors`
    ---
    https://developers.notion.com/reference/page-property-values#status
    """
    __slots__: typing.Sequence[str] = ('name')

    def __init__(self, status_option: Option, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'status')
        self.set('status', status_option)


class SelectPropertyValue(build.NotionObject, PagePropertyValue):
    """When selecting options, If the select database property does not yet have an option by the input name, 
    then the name will be added to the database schema if the integration also has write access to the parent database.

    NOTE: Commas (",") are not valid for select values.
    ---
    (required)
    :param select_option: a single select option: `notion.properties.Option` 
                             containing `name` and `notion.properties.PropertyColors`
    ---
    https://developers.notion.com/reference/page-property-values#select
    """
    __slots__: typing.Sequence[str] = ('name')

    def __init__(self, select_option: Option, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'select')
        self.set('select', select_option)


class MultiSelectPropertyValue(build.NotionObject, PagePropertyValue):
    """The MultiSelectPropertyValue contains an array of `notion.properties.Option` objects.

    When selecting options, If the multi-select database property does not yet have an option by the input name, 
    then the name will be added to the database schema if the integration also has write access to the parent database.

    NOTE: Commas (",") are not valid for select values.
    ---
    (required)  
    :param array_of_options: array of `notion.properties.Option` 
                             containing `name` and `notion.properties.PropertyColors`
    ---
    https://developers.notion.com/reference/page-property-values#multi-select
    """
    __slots__: typing.Sequence[str] = ('name')

    def __init__(self, array_of_options: list[Option], /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'multi_select')
        self.set('multi_select', array_of_options)


class CheckboxPropertyValue(build.NotionObject, PagePropertyValue):
    """
    (required)
    :param checkbox_value: Whether the checkbox is checked (true) or unchecked (false).
    ---
    https://developers.notion.com/reference/page-property-values#checkbox
    """
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, checkbox_value: bool, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'checkbox')
        self.set('checkbox', checkbox_value)


class PeoplePropertyValue(build.NotionObject, PagePropertyValue):
    """
    (required)
    :param array_of_users: An array of user objects.
            The Retrieve a page endpoint can't be guaranteed to return more than 25 people 
            per people page property. If a people page property includes more than 25 people, 
            then you can use the Retrieve a page property item endpoint for the specific 
            people property to get a complete list of people.
    ---
    https://developers.notion.com/reference/page-property-values#people
    """
    __slots__: typing.Sequence[str] = ('name')

    def __init__(self, array_of_users: list[UserObject], /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'people')
        self.set('people', array_of_users)


class RollupPropertyValue(build.NotionObject, PagePropertyValue):
    """
    (required)
    :param function: `notion.properties.FunctionsEnum`, function to update property to.
    ---
    If the results of the rollup is a date (e.g. function = latest date), the results
    will be a DatePropertyValue.
    If the results of the rollup is a number (e.g. function = sum), the results will be
    a NumberPropertyValue.
    If the results of the rollup is anything requireing multiple values (e.g. function = show original),
    the results will be an array object, with a key 'type' = 'array', 
    and key 'array' containing a list of values.
    
    NOTE: Only the function key can be updated via the API.
    ---
    https://developers.notion.com/reference/page-property-values#rollup
    """
    __slots__: typing.Sequence[str] = ('name', '_function')

    def __init__(self, function: FunctionsEnum, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self._function = build.NotionObject()
        self._function.set('function', function)

        self.set('type', 'rollup')
        self.set('rollup', self._function)


class EmailPropertyValue(build.NotionObject, PagePropertyValue):
    """https://developers.notion.com/reference/page-property-values#email"""
    __slots__: typing.Sequence[str] = ('name')

    def __init__(self, email: str, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'email')
        self.set('email', email)


class NumberPropertyValue(build.NotionObject, PagePropertyValue):
    """https://developers.notion.com/reference/page-property-values#number"""
    __slots__: typing.Sequence[str] = ('name')

    def __init__(self, number: float, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'number')
        self.set('number', number)


class PhoneNumberPropertyValue(build.NotionObject, PagePropertyValue):
    """
    (required)
    :param phone_number: A string representing a phone number. No phone number format is enforced.
    ---
    https://developers.notion.com/reference/page-property-values#phone-number"""
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, phone_number: float, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'phone_number')
        self.set('phone_number', phone_number)


class URLPropertyValue(build.NotionObject, PagePropertyValue):
    """https://developers.notion.com/reference/page-property-values#url"""
    __slots__: typing.Sequence[str] = ('name')
    
    def __init__(self, url: str, /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'url')
        self.set('url', url)
