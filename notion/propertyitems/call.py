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

import json
from datetime import datetime, tzinfo
from typing import Any, MutableMapping, Sequence, cast

from pytz import UnknownTimeZoneError, timezone

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


class PropertyItem:
    __slots__ = ("_map", "_type", "tz")

    def __init__(self, _map: MutableMapping[str, Any], tz: tzinfo) -> None:
        self._map = _map
        self._type = _map["type"]
        self.tz = tz

        if self._type == "property_item":
            self._type = _map["property_item"]["type"]

    def __repr__(self) -> str:
        return json.dumps(self._map)

    @property
    def item(self) -> Any:
        if self._type == "rollup":
            return self._map["property_item"]["rollup"]
        else:
            return self._map[self._type]

    @property
    def results(self) -> Any:
        assert self._map["object"] == "list"
        return self._map["results"]


def _assert_property_type(_property: PropertyItem, _type: str) -> TypeError | None:
    if _property._type != _type:
        raise TypeError(f"Expected type '{_type}', got '{_property._type}'")
    return None


def verification(_property: PropertyItem) -> bool:
    _assert_property_type(_property, "verification")
    match _property.item.state:
        case "verified":
            return True
        case _:
            return False


def checkbox(_property: PropertyItem) -> bool:
    _assert_property_type(_property, "checkbox")
    return cast(bool, _property.item)


def number(_property: PropertyItem) -> float:
    _assert_property_type(_property, "number")
    return cast(float, _property.item)


def date(_property: PropertyItem) -> datetime | tuple[datetime, datetime] | None:
    """
    :returns: If the property is a date range, returns a tuple of (start, end) dates.\
              Otherwise, returns a single start date.
    """
    _assert_property_type(_property, "date")
    return _retrieve_datetime(_property)


def select(_property: PropertyItem) -> str | None:
    """:returns: The name of the selected option."""
    _assert_property_type(_property, "select")
    item = _property.item
    if item:
        select: str | None = item.get("name")
        return select
    return None


def multi_select(_property: PropertyItem) -> list[str]:
    """:returns: A list of the names of the selected options."""
    _assert_property_type(_property, "multi_select")
    values = []
    for item in _property.item:
        select = item.get("name")
        if select:
            values.append(select)
    return values


def status(_property: PropertyItem) -> str:
    """:returns: The name of the selected status."""
    _assert_property_type(_property, "status")
    status: str = _property.item["name"]
    return status


def rich_text(_property: PropertyItem) -> str | None:
    _assert_property_type(_property, "rich_text")
    results = _property.results
    if results:
        text: str = results[0]["rich_text"]["plain_text"]
        return text
    return None


def number_formula(_property: PropertyItem) -> float | None:
    """:returns: The result of the formula. The formula property must return a number."""
    _assert_property_type(_property, "formula")

    formula_type = _property.item["type"]
    if formula_type == "number":
        number: float = _property.item.get("number")
        return number if number else None
    else:
        raise TypeError(f"Expected formula type 'number', got '{formula_type}'")


def string_formula(_property: PropertyItem) -> str | None:
    """:returns: The result of the formula. The formula property must return a string."""
    _assert_property_type(_property, "formula")

    formula_type = _property.item["type"]
    if formula_type == "string":
        string: str = _property.item.get("string")
        return string if string else None
    else:
        raise TypeError(f"Expected formula type 'string', got '{formula_type}'")


def boolean_formula(_property: PropertyItem) -> bool:
    """:returns: The result of the formula. The formula property must return a boolean."""
    _assert_property_type(_property, "formula")

    formula_type = _property.item["type"]
    if formula_type == "boolean":
        return cast(bool, _property.item["boolean"])
    else:
        raise TypeError(f"Expected formula type 'boolean', got '{formula_type}'")


def date_formula(
    _property: PropertyItem,
) -> datetime | tuple[datetime, datetime] | None:
    """:returns: The result of the formula. The formula property must return a date."""
    _assert_property_type(_property, "formula")

    formula_type = _property.item["type"]
    if formula_type == "date":
        return _retrieve_datetime(_property)
    else:
        raise TypeError(f"Expected formula type 'date', got '{formula_type}'")


def people(_property: PropertyItem) -> list[dict[str, Any]]:
    """:returns: A list of User mappings."""
    _assert_property_type(_property, "people")

    list_people = []
    for item in _property.results:
        list_people.append(item["people"])
    return list_people


def email(_property: PropertyItem) -> str | None:
    """:returns: The email address as a string."""
    _assert_property_type(_property, "email")
    email: str | None = _property.item
    return email


def phone_number(_property: PropertyItem) -> str | None:
    """:returns: The phone number as a string."""
    _assert_property_type(_property, "phone_number")
    phone_number: str | None = _property.item
    return phone_number


def url(_property: PropertyItem) -> str | None:
    """:returns: The URL as a string."""
    _assert_property_type(_property, "url")
    url: str | None = _property.item
    return url


def files(_property: PropertyItem) -> list[str]:
    """:returns: A list of URLs to the files."""
    _assert_property_type(_property, "files")

    file_urls: list[str] = []
    for file in _property.item:
        file_urls.append(file[file["type"]]["url"])
    return file_urls


def created_time(_property: PropertyItem) -> datetime:
    """:returns: The datetime the page was created."""
    _assert_property_type(_property, "created_time")
    return datetime.fromisoformat(_property._map["created_time"])


def created_by(_property: PropertyItem) -> dict[str, Any]:
    """:returns: The user who created the page."""
    _assert_property_type(_property, "created_by")
    return dict(_property.item)


def last_edited_time(_property: PropertyItem) -> datetime:
    """:returns: The datetime the page was last edited."""
    _assert_property_type(_property, "last_edited_time")
    return datetime.fromisoformat(_property._map["last_edited_time"])


def last_edited_by(_property: PropertyItem) -> dict[str, Any]:
    """:returns: The user who last edited the page."""
    _assert_property_type(_property, "last_edited_by")
    return dict(_property.item)


def relation(_property: PropertyItem) -> list[str]:
    """:returns: A list of page IDs that are related to the page."""
    _assert_property_type(_property, "relation")
    return [_page["relation"]["id"] for _page in _property.results]


UNSUPPORTED_ROLLUP_AGGREGATIONS = [
    "show_original",
    "show_unique",
    "median",
    "percent_per_group",
    "count_per_group",
]


def number_rollup(_property: PropertyItem) -> float:
    """:returns: The result of the rollup. The rollup property must return a number."""
    _assert_property_type(_property, "rollup")

    ftype: str = _property._map["property_item"]["rollup"]["function"]
    if ftype in UNSUPPORTED_ROLLUP_AGGREGATIONS:
        raise not_implemented_error(ftype)

    if _property._map["property_item"]["rollup"]["type"] == "number":
        return cast(float, _property._map["property_item"]["rollup"]["number"])

    raise TypeError("rollup type is not number.")


def date_rollup(
    _property: PropertyItem,
) -> datetime | tuple[datetime, datetime] | None:
    """ 
    :returns: The result of the rollup. The rollup property must return a date.\
              If the rollup is a date range, a tuple of (start, end) is returned.\
              Otherwise, a single datetime is returned.
    """
    _assert_property_type(_property, "rollup")

    ftype: str = _property._map["property_item"]["rollup"]["function"]
    if ftype in UNSUPPORTED_ROLLUP_AGGREGATIONS:
        raise not_implemented_error(ftype)

    if _property._map["property_item"]["rollup"]["type"] == "date":
        return _retrieve_datetime(_property)

    raise TypeError("rollup type is not date.")


def not_implemented_error(notion_function: str) -> NotImplementedError:
    if notion_function == "show_original":
        return NotImplementedError(
            "`show_original` rollup calculation is not yet implemented."
        )
    return NotImplementedError(f"Unsupported rollup aggregation: {notion_function}.")


def _retrieve_datetime(
    _property: PropertyItem,
) -> datetime | tuple[datetime, datetime] | None:
    if _property._type in ("rollup", "formula"):
        date = _property.item["date"]
    else:
        date = _property.item

    if date is None:
        return None

    start = date["start"]
    end = date["end"]
    time_zone = date["time_zone"]

    if time_zone is not None:
        try:
            time_zone = timezone(time_zone)
        except UnknownTimeZoneError:
            pass
    if time_zone is None:
        time_zone = _property.tz

    start = datetime.fromisoformat(start)
    if end is not None:
        end = datetime.fromisoformat(end)
    if time_zone is not None:
        start = start.astimezone(time_zone)
        if end:
            end = end.astimezone(time_zone)
            return (start, end)
    if start and end:
        return (start, end)
    else:
        assert isinstance(start, datetime)
        return start
