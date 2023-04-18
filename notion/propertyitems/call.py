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

from datetime import datetime
from typing import Sequence, TypeVar, cast

from notion.propertyitems.base import (
    NOT_IMPLEMENTED_ERR,
    NOT_IMPLEMENTED_FUNCTIONS,
    PropertyItem,
    UserPropertyItem,
    _assert_property_type,
    _function_type,
    _map_user,
    _retrieve_datetime,
)

__all__: Sequence[str] = (
    "checkbox",
    "number",
    "date",
    "select",
    "multi_select",
    "status",
    "rich_text",
    "people",
    "email",
    "phone_number",
    "url",
    "files",
    "created_by",
    "created_time",
    "last_edited_time",
    "last_edited_by",
    "number_formula",
    "string_formula",
    "boolean_formula",
    "date_formula",
    "relation",
    "number_rollup",
    "date_rollup",
)

T_PropertyItem = TypeVar("T_PropertyItem", bound=PropertyItem)


def checkbox(property: T_PropertyItem) -> bool:
    _assert_property_type(property, "checkbox")
    return cast(bool, property.item)


def number(property: T_PropertyItem) -> float:
    _assert_property_type(property, "number")
    return cast(float, property.item)


def date(property: T_PropertyItem) -> datetime | tuple[datetime, datetime]:
    """
    :returns: If the property is a date range, returns a tuple of (start, end) dates.\
              Otherwise, returns a single start date.
    """
    _assert_property_type(property, "date")
    return _retrieve_datetime(property)


def select(property: T_PropertyItem) -> str:
    """:returns: The name of the selected option."""
    _assert_property_type(property, "select")
    return str(property.item["name"])


def multi_select(property: T_PropertyItem) -> list[str]:
    """:returns: A list of the names of the selected options."""
    _assert_property_type(property, "multi_select")
    return [str(select["name"]) for select in property.item]


def status(property: T_PropertyItem) -> str:
    """:returns: The name of the selected status."""
    _assert_property_type(property, "status")
    return str(property.item["name"])


def rich_text(property: T_PropertyItem) -> str:
    _assert_property_type(property, "rich_text")
    return str(property.results[0]["rich_text"]["plain_text"])


def number_formula(property: T_PropertyItem) -> float:
    """:returns: The result of the formula. The formula property must return a number."""
    _assert_property_type(property, "formula")

    formula_type = property.item["type"]
    if formula_type == "number":
        return float(property.item["number"])
    else:
        raise TypeError(f"Expected formula type 'number', got '{formula_type}'")


def string_formula(property: T_PropertyItem) -> str:
    """:returns: The result of the formula. The formula property must return a string."""
    _assert_property_type(property, "formula")

    formula_type = property.item["type"]
    if formula_type == "string":
        return str(property.item["string"])
    else:
        raise TypeError(f"Expected formula type 'string', got '{formula_type}'")


def boolean_formula(property: T_PropertyItem) -> bool:
    """:returns: The result of the formula. The formula property must return a boolean."""
    _assert_property_type(property, "formula")

    formula_type = property.item["type"]
    if formula_type == "boolean":
        return bool(property.item["boolean"])
    else:
        raise TypeError(f"Expected formula type 'boolean', got '{formula_type}'")


def date_formula(property: T_PropertyItem) -> datetime | tuple[datetime, datetime]:
    """:returns: The result of the formula. The formula property must return a date."""
    _assert_property_type(property, "formula")

    formula_type = property.item["type"]
    if formula_type == "date":
        return _retrieve_datetime(property)
    else:
        raise TypeError(f"Expected formula type 'date', got '{formula_type}'")


def people(property: T_PropertyItem) -> list[UserPropertyItem]:
    """:returns: A list of UserPropertyItem objects."""
    _assert_property_type(property, "people")

    list_people = []
    for user in property.results:
        list_people.append(_map_user(user))
    return list_people


def email(property: T_PropertyItem) -> str:
    """:returns: The email address as a string."""
    _assert_property_type(property, "email")
    return str(property.item)


def phone_number(property: T_PropertyItem) -> str:
    """:returns: The phone number as a string."""
    _assert_property_type(property, "phone_number")
    return str(property.item)


def url(property: T_PropertyItem) -> str:
    """:returns: The URL as a string."""
    _assert_property_type(property, "url")
    return str(property.item)


def files(property: T_PropertyItem) -> list[str]:
    """:returns: A list of URLs to the files."""
    _assert_property_type(property, "files")

    file_urls: list[str] = []
    for file in property.item:
        file_urls.append(file[file["type"]]["url"])
    return file_urls


def created_time(property: T_PropertyItem) -> datetime:
    """:returns: The datetime the page was created."""
    _assert_property_type(property, "created_time")
    return datetime.fromisoformat(str(property.map["created_time"]))


def created_by(property: T_PropertyItem) -> UserPropertyItem:
    """:returns: The user who created the page."""
    _assert_property_type(property, "created_by")
    return _map_user(property)


def last_edited_time(property: T_PropertyItem) -> datetime:
    """:returns: The datetime the page was last edited."""
    _assert_property_type(property, "last_edited_time")
    return datetime.fromisoformat(str(property.map["last_edited_time"]))


def last_edited_by(property: T_PropertyItem) -> UserPropertyItem:
    """:returns: The user who last edited the page."""
    _assert_property_type(property, "last_edited_by")
    return _map_user(property)


def relation(property: T_PropertyItem) -> list[str]:
    """:returns: A list of page IDs that are related to the page."""
    _assert_property_type(property, "relation")
    return [_page["relation"]["id"] for _page in property.results]


def number_rollup(property: T_PropertyItem) -> float:
    """:returns: The result of the rollup. The rollup property must return a number."""
    _assert_property_type(property, "rollup")
    if (func := _function_type(property)) in NOT_IMPLEMENTED_FUNCTIONS:
        raise NOT_IMPLEMENTED_ERR(func)

    if property.map["property_item"]["rollup"]["type"] == "number":
        return cast(float, property.map["property_item"]["rollup"]["number"])
    else:
        raise TypeError("rollup type is not number.")


def date_rollup(property: T_PropertyItem) -> datetime | tuple[datetime, datetime]:
    """ 
    :returns: The result of the rollup. The rollup property must return a date.\
              If the rollup is a date range, a tuple of (start, end) is returned.\
              Otherwise, a single datetime is returned.
    """
    _assert_property_type(property, "rollup")
    if (func := _function_type(property)) in NOT_IMPLEMENTED_FUNCTIONS:
        raise NOT_IMPLEMENTED_ERR(func)

    if property.map["property_item"]["rollup"]["type"] == "date":
        return _retrieve_datetime(property)

    raise TypeError("rollup type is not date.")
