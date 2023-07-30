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

NOTE: The following property values cannot be updated directly via the API and are excluded.
- Created By
- Created Time
- Last Edited By
- Last Edited Time
- Formula property value objects represent the result of evaluating a formula described in the
    database's properties. They contain a formula object with a type of either boolean/date/number/string.
    The value can't be updated directly via the API.

FilesPropertyValue can be found in `notion.properties.files`.

https://developers.notion.com/reference/page-property-values
"""
from __future__ import annotations

from abc import ABCMeta
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Sequence

from notion.properties.build import NotionObject
from notion.properties.common import UserObject, _NotionUUID
from notion.properties.options import FunctionFormat
from notion.properties.propertyobjects import Option, PropertyObject
from notion.properties.richtext import Mention, RichText

if TYPE_CHECKING:
    from datetime import timedelta

__all__: Sequence[str] = (
    "Properties",
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


class PagePropertyValue(metaclass=ABCMeta):
    def __init__(self, property_name: str) -> None:
        self.name = property_name


class Properties(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, *properties: PropertyObject | PagePropertyValue) -> None:
        """
        A page object is made up of page properties that contain data about the page.
        When you send a request to Create a page, you set the page properties in the properties object body param.
        Retrieve a page gets the identifier, type, and value of a page's properties.
        Retrieve a page property item returns information about a single property ID.

        https://developers.notion.com/reference/page-property-values"""
        super().__init__()
        for prop in properties:
            if not hasattr(prop, "name"):
                raise AttributeError("Missing attribute `property_name`")

            if isinstance(prop, TitlePropertyValue):
                self.nest("properties", prop.name, prop.get("title"))
            else:
                self.nest("properties", prop.name, prop)


class RichTextPropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(
        self, property_name: str, /, rich_text: Sequence[RichText | Mention]
    ) -> None:
        """
        The purpose of the rich text property value is to provide the key `rich_text`,
        whereas the object `notion.properties.RichText` has the key `text`.

        :param rich_text: (required) An array of rich text objects.

        The RichText Object: https://developers.notion.com/reference/rich-text
        The RichText Property Value: https://developers.notion.com/reference/page-property-values#rich-text
        """
        super().__init__(property_name=property_name)
        self.set("type", "rich_text")
        self.set("rich_text", rich_text)


class TitlePropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, title_: Sequence[RichText | Mention]) -> None:
        """
        :param title: (required) An array of rich text objects

        https://developers.notion.com/reference/page-property-values#title
        """
        super().__init__(property_name="title")
        self.set_array(self.name, title_)


class DatePropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(
        self,
        property_name: str,
        /,
        *,
        start: str | datetime,
        end: Optional[str | datetime] = None,
    ) -> None:
        """
        Notion uses ISO 8601 date and time for some endpoints, and YYYY/MM/DD for others.
        If a datetime object is passed to either parameter, they'll be converted to isoformat.

        ---
        :param start: (required) A date, with an optional time.\
                       If the "date" value is a range, then start represents the start of the range.
        :param end: (optional) A string representing the end of a date range.\
                     If the value is null, then the date value is not a range.

        https://developers.notion.com/reference/page-property-values#date
        """
        super().__init__(property_name=property_name)
        self.nest("date", "start", start)
        self.nest("date", "end", end) if end else None


class RelationPropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, related_ids: Sequence[_NotionUUID]) -> None:
        """
        NOTE: updating a relation property value with an empty array will clear the list.

        ---
        :param related_ids: (required) An array of related page references.\
                             A page reference is an object with an id key and a string value (UUIDv4)\
                             corresponding to a page ID in another database.

        https://developers.notion.com/reference/page-property-values#relation
        """
        super().__init__(property_name=property_name)
        self.set("type", "relation")
        self.set("relation", [id for id in related_ids])


class StatusPropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, status_option: Option) -> None:
        """
        :param status_option: (required) a single status option: `notion.properties.Option`\
                               containing `name` and `notion.properties.PropertyColor`

        https://developers.notion.com/reference/page-property-values#status
        """
        super().__init__(property_name=property_name)
        self.set("type", "status")
        self.set("status", status_option)


class SelectPropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, select_option: Option) -> None:
        """
        When selecting options, If the select database property does not yet have an option by the input name,
        then the name will be added to the database schema if the integration also has write access to the parent database.
        
        ---
        :param select_option: (required) a single select option: `notion.properties.Option`\
                               containing `name` and `notion.properties.PropertyColor`\
                               NOTE: Commas (",") are not valid for select values.

        https://developers.notion.com/reference/page-property-values#select
        """
        super().__init__(property_name=property_name)
        self.set("type", "select")
        self.set("select", select_option)


class MultiSelectPropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, options_array: Sequence[Option]) -> None:
        """
        The MultiSelectPropertyValue contains an array of `notion.properties.Option` objects.
        When selecting options, If the multi-select database property does not yet have an option by the input name,
        then the name will be added to the database schema if the integration also has write access to the parent database.

        ---
        :param options_array: (required) array of `notion.properties.Option`\
                               containing `name` and `notion.properties.PropertyColor`\
                               NOTE: Commas (",") are not valid for select values.

        https://developers.notion.com/reference/page-property-values#multi-select
        """
        super().__init__(property_name=property_name)
        self.set("type", "multi_select")
        self.set("multi_select", options_array)


class CheckboxPropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, checkbox_value: bool) -> None:
        """https://developers.notion.com/reference/page-property-values#checkbox"""
        super().__init__(property_name=property_name)
        self.set("type", "checkbox")
        self.set("checkbox", checkbox_value)


class PeoplePropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, user_array: Sequence[UserObject]) -> None:
        """
        :param user_array: (required) An array of user objects.\
                            The Retrieve a page endpoint can't be guaranteed to return more than 25 people\
                            per people page property. If a people page property includes more than 25 people,\
                            then you can use the Retrieve a page property item endpoint for the specific
                            people property to get a complete list of people.

        https://developers.notion.com/reference/page-property-values#people
        """
        super().__init__(property_name=property_name)
        self.set("type", "people")
        self.set("people", user_array)


class RollupPropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, function: FunctionFormat | str) -> None:
        """
        If the results of the rollup is a date (e.g. function = latest date),
        the results will be a DatePropertyValue.

        If the results of the rollup is a number (e.g. function = sum),
        the results will be a NumberPropertyValue.

        If the results of the rollup is anything requireing multiple values (e.g. function = show original),
        the results will be an array object, with a key 'type' = 'array', and key 'array' containing a list of values.

        NOTE: Only the function key can be updated via the API.

        https://developers.notion.com/reference/page-property-values#rollup
        """
        super().__init__(property_name=property_name)
        self.set("type", "rollup")
        self.nest("rollup", "function", function)


class EmailPropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, email: str) -> None:
        """https://developers.notion.com/reference/page-property-values#email"""
        super().__init__(property_name=property_name)
        self.set("type", "email")
        self.set("email", email)


class NumberPropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, number: int | float | timedelta) -> None:
        """https://developers.notion.com/reference/page-property-values#number"""
        super().__init__(property_name=property_name)
        self.set("type", "number")
        self.set("number", number)


class PhoneNumberPropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, phone_number: str) -> None:
        """https://developers.notion.com/reference/page-property-values#phone-number"""
        super().__init__(property_name=property_name)
        self.set("type", "phone_number")
        self.set("phone_number", phone_number)


class URLPropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, url: str) -> None:
        """https://developers.notion.com/reference/page-property-values#url"""
        super().__init__(property_name=property_name)
        self.set("type", "url")
        self.set("url", url)
