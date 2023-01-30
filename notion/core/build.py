import typing

import json

from notion.core.typedefs import *
from notion.core.typedefs import DateISO8601
from notion.core.typedefs import PagePropertyValue
from notion.core.typedefs import PropertyObject
from notion.core.typedefs import BlockTypeObjects

__all__: typing.Sequence[str] = ('NotionObject', 'request_json')

T = typing.TypeVar("T")
T_co = typing.TypeVar("T_co", covariant=True)


@typing.overload
def request_json(*objects: PagePropertyValue, final: dict[str, JSONish] = {}) -> JSONObject: ...
@typing.overload
def request_json(*objects: PropertyObject, final: dict[str, JSONish] = {}) -> JSONObject: ...
@typing.overload
def request_json(*objects: BlockTypeObjects, final: dict[str, JSONish] = {}) -> JSONObject: ...
@typing.overload
def request_json(*objects: DateISO8601, final: dict[str, JSONish] = {}) -> JSONObject: ...
@typing.overload
def request_json(*objects: JSONObject, final: dict[str, JSONish] = {}) -> JSONObject: ...
@typing.overload
def request_json(*objects: JSONish, final: dict[str, JSONish] = {}) -> JSONObject: ...
@typing.overload
def request_json(*objects: JSONPayload, final: dict[str, JSONish] = {}) -> JSONObject: ...

def request_json(*objects, final = {})  -> JSONish:
	{final.update(x) for x in objects}
	return json.dumps(final, indent=4)


class NotionObject(typing.Dict[str, JSONish]):
    __slots__: typing.Sequence[str] = ()

    def __init__(self) -> None:
        super().__init__()

    @typing.overload
    def set(self, key: str, value: PagePropertyValue, /) -> None: ...
    @typing.overload
    def set(self, key: str, value: PropertyObject, /) -> None: ...
    @typing.overload
    def set(self, key: str, value: BlockTypeObjects, /) -> None: ...
    @typing.overload
    def set(self, key: str, value: typing.MutableMapping[str, str], /) -> None: ...
    @typing.overload
    def set(self, key: str, value: DateISO8601, /) -> None: ...
    @typing.overload
    def set(self, key: str, value: JSONObject, /) -> None: ...
    @typing.overload
    def set(self, key: str, value: JSONish, /) -> None: ...

    def set(self, key, value, /) -> None:
        self[key] = value

    @typing.overload
    def set_array( self, key: str, values: typing.Iterable[JSONish], /) -> None: ...
    @typing.overload
    def set_array(self, key: str, values: typing.Iterable[T_co], /, *, 
                  conversion: typing.Callable[[T_co], JSONish]) -> None: ...

    def set_array(self, key: str, values: typing.Iterable[typing.Any], 
                  /, *, conversion: typing.Optional[typing.Callable[[typing.Any], JSONish]] = None) -> None:
        if conversion is not None:
            self[key] = [conversion(value) for value in values]
        else:
            self[key] = list(values)
