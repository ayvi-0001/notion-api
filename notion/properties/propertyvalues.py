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

import abc
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Sequence, Union

from notion.properties.build import NotionObject
from notion.properties.common import NotionUUID, UserObject
from notion.properties.options import FunctionFormat
from notion.properties.propertyobjects import Option
from notion.properties.richtext import Equation, Mention, RichText

if TYPE_CHECKING:
    from datetime import timedelta

__all__: Sequence[str] = (
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


class PagePropertyValue(metaclass=abc.ABCMeta):
    def __init__(self, property_name: str) -> None:
        self.name = property_name


class RichTextPropertyValue(PagePropertyValue, NotionObject):
    r"""
    The purpose of the rich text property value is to provide the key `rich_text`, whereas the object
    `notion.properties.RichText` has the key `text`.
    ---
    (required)
    :param rich_text_array: An array of rich text objects.
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
    __slots__: Sequence[str] = ["name"]

    def __init__(
        self,
        property_name: str,
        rich_text_array: Sequence[Union[RichText, Mention, Equation]],
        /,
    ) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "rich_text")
        self.set("rich_text", rich_text_array)


class TitlePropertyValue(PagePropertyValue, NotionObject):
    """
    :param title: (required) An array of rich text objects: `notion.properties.propertyvalues.RichText`

    ---
    https://developers.notion.com/reference/page-property-values#title
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(self, title_: Sequence[Union[RichText, Mention, Equation]], /) -> None:
        super().__init__(property_name="title")
        self.set_array(self.name, title_)


class DatePropertyValue(PagePropertyValue, NotionObject):
    """
    Notion uses ISO 8601 date and time for some endpoints, and YYYY/MM/DD for others.
    If a datetime object is passed to either parameter, they'll be converted to isoformat.

    ---
    :param start: (required) A date, with an optional time.
        If the "date" value is a range, then start represents the start of the range.
    :param end: (optional) A string representing the end of a date range.
        If the value is null, then the date value is not a range.

    https://developers.notion.com/reference/page-property-values#date
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(
        self,
        property_name: str,
        /,
        *,
        start: Union[str, datetime],
        end: Optional[Union[str, datetime]] = None,
    ) -> None:
        super().__init__(property_name=property_name)

        self.nest("date", "start", start)
        self.nest("date", "end", end) if end else None


class RelationPropertyValue(PagePropertyValue, NotionObject):
    """
    NOTE: updating a relation property value with an empty array will clear the list.

    ---
    :param related_ids: (required) An array of related page references.
        A page reference is an object with an id key and a string value (UUIDv4)
        corresponding to a page ID in another database.

    :param has_more: (optional) If a relation has more than 25 references, then the has_more value for
        the relation in the response object is true. If a relation doesn't
        exceed the limit, then has_more is false.

    https://developers.notion.com/reference/page-property-values#relation
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(
        self,
        property_name: str,
        *related_ids: list[NotionUUID],
        has_more: Optional[bool] = None,
    ) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "relation")
        self.set("relation", [x for x in related_ids][0])
        if has_more:
            self.set("has_more", True)


class StatusPropertyValue(PagePropertyValue, NotionObject):
    """
    :param status_option: (required) a single status option: `notion.properties.Option`
        containing `name` and `notion.properties.PropertyColor`

    https://developers.notion.com/reference/page-property-values#status
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, status_option: Option, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "status")
        self.set("status", status_option)


class SelectPropertyValue(PagePropertyValue, NotionObject):
    """
    When selecting options, If the select database property does not yet have an option by the input name,
    then the name will be added to the database schema if the integration also has write access to the parent database.
    NOTE: Commas (",") are not valid for select values.

    ---
    :param select_option: (required) a single select option: `notion.properties.Option`
        containing `name` and `notion.properties.PropertyColor`

    https://developers.notion.com/reference/page-property-values#select
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, select_option: Option, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "select")
        self.set("select", select_option)


class MultiSelectPropertyValue(PagePropertyValue, NotionObject):
    """
    The MultiSelectPropertyValue contains an array of `notion.properties.Option` objects.
    When selecting options, If the multi-select database property does not yet have an option by the input name,
    then the name will be added to the database schema if the integration also has write access to the parent database.
    NOTE: Commas (",") are not valid for select values.

    ---
    :param options_array: (required) array of `notion.properties.Option`
        containing `name` and `notion.properties.PropertyColor`

    https://developers.notion.com/reference/page-property-values#multi-select
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, options_array: list[Option], /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "multi_select")
        self.set("multi_select", options_array)


class CheckboxPropertyValue(PagePropertyValue, NotionObject):
    """
    :param checkbox_value: (required) Whether the checkbox is checked (true) or unchecked (false).

    https://developers.notion.com/reference/page-property-values#checkbox
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, checkbox_value: bool, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "checkbox")
        self.set("checkbox", checkbox_value)


class PeoplePropertyValue(PagePropertyValue, NotionObject):
    """
    :param user_array: (required) An array of user objects.
        The Retrieve a page endpoint can't be guaranteed to return more than 25 people
        per people page property. If a people page property includes more than 25 people,
        then you can use the Retrieve a page property item endpoint for the specific
        people property to get a complete list of people.

    https://developers.notion.com/reference/page-property-values#people
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, user_array: list[UserObject], /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "people")
        self.set("people", user_array)


class RollupPropertyValue(PagePropertyValue, NotionObject):
    """
    :param function: (required) `notion.properties.FunctionFormat`, function to update property to.

    ---
    If the results of the rollup is a date (e.g. function = latest date), the results
    will be a DatePropertyValue.
    If the results of the rollup is a number (e.g. function = sum), the results will be
    a NumberPropertyValue.
    If the results of the rollup is anything requireing multiple values (e.g. function = show original),
    the results will be an array object, with a key 'type' = 'array',
    and key 'array' containing a list of values.

    NOTE: Only the function key can be updated via the API.

    https://developers.notion.com/reference/page-property-values#rollup
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, function: FunctionFormat, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "rollup")
        self.nest("rollup", "function", function)


class EmailPropertyValue(PagePropertyValue, NotionObject):
    """https://developers.notion.com/reference/page-property-values#email"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, email: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "email")
        self.set("email", email)


class NumberPropertyValue(PagePropertyValue, NotionObject):
    """https://developers.notion.com/reference/page-property-values#number"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, number: Union[float, timedelta], /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "number")
        self.set("number", number)


class PhoneNumberPropertyValue(PagePropertyValue, NotionObject):
    """
    :param phone_number: (required) A string representing a phone number.
        No phone number format is enforced.

    https://developers.notion.com/reference/page-property-values#phone-number
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, phone_number: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "phone_number")
        self.set("phone_number", phone_number)


class URLPropertyValue(PagePropertyValue, NotionObject):
    """https://developers.notion.com/reference/page-property-values#url"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, url: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "url")
        self.set("url", url)
