import typing

import orjson

from notion.core.typedefs import *

__all__: typing.Sequence[str] = ('NotionObject', 'request_json')

_KT = typing.TypeVar("_KT")
_VT = typing.TypeVar("_VT")


@typing.final
def request_json(*objects: typing.MutableMapping) -> typing.Union[JSONPayload, JSONObject]:
    final: typing.MutableMapping = {}
    for x in objects:
        final |= x
    return orjson.dumps(final)


class NotionObject(typing.Dict[str, JSON], typing.Generic[_KT, _VT]):
    __slots__: typing.Sequence[str] = ()

    def __init__(self) -> None:
        super().__init__()
    
    @typing.overload
    def set(self, key: str, value: JSONPayload) -> None: ...
    @typing.overload
    def set(self, key: str, value: JSONObject) -> None: ...
    @typing.overload
    def set(self, key: str, value: JSON) -> None: ...
    @typing.overload
    def set(self, key: str, value: typing.MutableMapping) -> None: ...

    def set(self, key, value) -> None:
        self[key] = value

    @typing.final
    def nest(self, key, k: _KT, v: _VT) -> None:
        if key not in self.keys():
            self.set(key, {k:v})
        else:
            self[key] |= {k:v} #type: ignore[assignment]
    
    @typing.final
    def set_array(self, key: str, values: typing.Union[typing.Iterable[typing.Any], JSONObject], /) -> None:
        self[key] = list(values)
