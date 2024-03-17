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
from typing import Sequence, cast

from notion.propertyitems import base

__all__: Sequence[str] = (
    "verification",
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


def verification(_property: base.PropertyItem) -> bool:
    base._assert_property_type(_property, "verification")
    match _property.item.state:
        case "verified":
            return True
        case _:
            return False


def checkbox(_property: base.PropertyItem) -> bool:
    base._assert_property_type(_property, "checkbox")
    return cast(bool, _property.item)


def number(_property: base.PropertyItem) -> float:
    base._assert_property_type(_property, "number")
    return cast(float, _property.item)


def date(_property: base.PropertyItem) -> datetime | tuple[datetime, datetime]:
    """
    :returns: If the property is a date range, returns a tuple of (start, end) dates.\
              Otherwise, returns a single start date.
    """
    base._assert_property_type(_property, "date")
    return base._retrieve_datetime(_property)


def select(_property: base.PropertyItem) -> str:
    """:returns: The name of the selected option."""
    base._assert_property_type(_property, "select")
    return f"{_property.item['name']}"


def multi_select(_property: base.PropertyItem) -> list[str]:
    """:returns: A list of the names of the selected options."""
    base._assert_property_type(_property, "multi_select")
    return [f"{select['name']}" for select in _property.item]


def status(_property: base.PropertyItem) -> str:
    """:returns: The name of the selected status."""
    base._assert_property_type(_property, "status")
    return f"{_property.item['name']}"


def rich_text(_property: base.PropertyItem) -> str:
    base._assert_property_type(_property, "rich_text")
    return f"{_property.results[0]['rich_text']['plain_text']}"


def number_formula(_property: base.PropertyItem) -> float:
    """:returns: The result of the formula. The formula property must return a number."""
    base._assert_property_type(_property, "formula")

    formula_type = _property.item["type"]
    if formula_type == "number":
        return float(_property.item["number"])
    else:
        raise TypeError(f"Expected formula type 'number', got '{formula_type}'")


def string_formula(_property: base.PropertyItem) -> str:
    """:returns: The result of the formula. The formula property must return a string."""
    base._assert_property_type(_property, "formula")

    formula_type = _property.item["type"]
    if formula_type == "string":
        return f"{_property.item['string']}"
    else:
        raise TypeError(f"Expected formula type 'string', got '{formula_type}'")


def boolean_formula(_property: base.PropertyItem) -> bool:
    """:returns: The result of the formula. The formula property must return a boolean."""
    base._assert_property_type(_property, "formula")

    formula_type = _property.item["type"]
    if formula_type == "boolean":
        return bool(_property.item["boolean"])
    else:
        raise TypeError(f"Expected formula type 'boolean', got '{formula_type}'")


def date_formula(_property: base.PropertyItem) -> datetime | tuple[datetime, datetime]:
    """:returns: The result of the formula. The formula property must return a date."""
    base._assert_property_type(_property, "formula")

    formula_type = _property.item["type"]
    if formula_type == "date":
        return base._retrieve_datetime(_property)
    else:
        raise TypeError(f"Expected formula type 'date', got '{formula_type}'")


def people(_property: base.PropertyItem) -> list[base.UserPropertyItem]:
    """:returns: A list of Userbase.PropertyItem objects."""
    base._assert_property_type(_property, "people")

    list_people = []
    for user in _property.results:
        list_people.append(base._map_user(user))
    return list_people


def email(_property: base.PropertyItem) -> str:
    """:returns: The email address as a string."""
    base._assert_property_type(_property, "email")
    return f"{_property.item}"


def phone_number(_property: base.PropertyItem) -> str:
    """:returns: The phone number as a string."""
    base._assert_property_type(_property, "phone_number")
    return f"{_property.item}"


def url(_property: base.PropertyItem) -> str:
    """:returns: The URL as a string."""
    base._assert_property_type(_property, "url")
    return f"{_property.item}"


def files(_property: base.PropertyItem) -> list[str]:
    """:returns: A list of URLs to the files."""
    base._assert_property_type(_property, "files")

    file_urls: list[str] = []
    for file in _property.item:
        file_urls.append(file[file["type"]]["url"])
    return file_urls


def created_time(_property: base.PropertyItem) -> datetime:
    """:returns: The datetime the page was created."""
    base._assert_property_type(_property, "created_time")
    return datetime.fromisoformat(f"{_property._map['created_time']}")


def created_by(_property: base.PropertyItem) -> base.UserPropertyItem:
    """:returns: The user who created the page."""
    base._assert_property_type(_property, "created_by")
    return base._map_user(_property)


def last_edited_time(_property: base.PropertyItem) -> datetime:
    """:returns: The datetime the page was last edited."""
    base._assert_property_type(_property, "last_edited_time")
    return datetime.fromisoformat(f"{_property._map['last_edited_time']}")


def last_edited_by(_property: base.PropertyItem) -> base.UserPropertyItem:
    """:returns: The user who last edited the page."""
    base._assert_property_type(_property, "last_edited_by")
    return base._map_user(_property)


def relation(_property: base.PropertyItem) -> list[str]:
    """:returns: A list of page IDs that are related to the page."""
    base._assert_property_type(_property, "relation")
    return [_page["relation"]["id"] for _page in _property.results]


def number_rollup(_property: base.PropertyItem) -> float:
    """:returns: The result of the rollup. The rollup property must return a number."""
    base._assert_property_type(_property, "rollup")
    if (func := base._function_type(_property)) in base.NOT_IMPLEMENTED_FUNCTIONS:
        raise base.NOT_IMPLEMENTED_ERR(func)

    if _property._map["property_item"]["rollup"]["type"] == "number":
        return cast(float, _property._map["property_item"]["rollup"]["number"])

    raise TypeError("rollup type is not number.")


def date_rollup(_property: base.PropertyItem) -> datetime | tuple[datetime, datetime]:
    """ 
    :returns: The result of the rollup. The rollup property must return a date.\
              If the rollup is a date range, a tuple of (start, end) is returned.\
              Otherwise, a single datetime is returned.
    """
    base._assert_property_type(_property, "rollup")
    if (func := base._function_type(_property)) in base.NOT_IMPLEMENTED_FUNCTIONS:
        raise base.NOT_IMPLEMENTED_ERR(func)

    if _property._map["property_item"]["rollup"]["type"] == "date":
        return base._retrieve_datetime(_property)

    raise TypeError("rollup type is not date.")
