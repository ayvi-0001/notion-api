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

from dataclasses import dataclass
from datetime import datetime
from typing import Any, MutableMapping, Optional, Sequence, cast

import pytz

__all__: Sequence[str] = (
    "PropertyItem",
    "UserPropertyItem",
    "_map_user",
    "_function_type",
    "_retrieve_datetime",
    "_assert_property_type",
    "NOT_IMPLEMENTED_ERR",
)


class PropertyItem:
    def __init__(self, _map: MutableMapping[str, Any], source_page: str) -> None:
        self._map = _map
        self.source_page = source_page
        self._type = _map["type"]

        if self._type == "property_item":
            self._type = _map["property_item"]["type"]

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


@dataclass
class UserPropertyItem:
    id: str
    name: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    bot: Optional[dict[str, None]] = None


def _map_user(_property: PropertyItem) -> UserPropertyItem:
    if _property.item["type"] == "person":
        email = _property.item["person"]["email"]
        avatar_url = _property.item["avatar_url"]

        return UserPropertyItem(
            id=_property.item["id"],
            name=_property.item["name"],
            email=email if email else None,
            avatar_url=avatar_url if avatar_url else None,
        )

    else:
        avatar_url = _property.item["avatar_url"]

        return UserPropertyItem(
            id=_property.item["id"],
            name=_property.item["name"],
            bot=_property.item["bot"],
            avatar_url=avatar_url if avatar_url else None,
        )


def _function_type(_property: PropertyItem) -> str:
    return cast(str, _property._map["property_item"]["rollup"]["function"])


def _retrieve_datetime(_property: PropertyItem) -> datetime | tuple[datetime, datetime]:
    if _property._type in ("rollup", "formula"):
        date = _property.item["date"]
        start = date["start"]
        end = date["end"]
        time_zone = date["time_zone"]
    else:
        start = _property.item["start"]
        end = _property.item["end"]
        time_zone = _property.item["time_zone"]

    start = datetime.fromisoformat(f"{start}")
    if end is not None:
        end = datetime.fromisoformat(f"{end}")
    if time_zone is not None:
        start = start.astimezone(tz=pytz.timezone(time_zone))
        if end:
            end = end.astimezone(tz=pytz.timezone(time_zone))
            return (start, end)
    if start and end:
        return (start, end)
    else:
        assert isinstance(start, datetime)
        return start


def _assert_property_type(_property: PropertyItem, t: str) -> TypeError | None:
    if _property._type != t:
        raise TypeError(f"Expected type '{t}', got '{_property._type}'")
    return None


NOT_IMPLEMENTED_FUNCTIONS = [
    "show_original",
    "show_unique",
    "median",
    "percent_per_group",
    "count_per_group",
]


def NOT_IMPLEMENTED_ERR(notion_function: str) -> NotImplementedError:
    if notion_function == "show_original":
        return NotImplementedError("`show_original` is not yet implemented.")

    return NotImplementedError(
        "`%s` function is not supported by Notion's property items." % notion_function
    )
