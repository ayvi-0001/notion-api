from typing import Union
from typing import Generic
from typing import Sequence
from typing import TypeVar
from typing import Iterable
from typing import Any

import orjson

from notion.core.typedefs import *

__all__: Sequence[str] = ("NotionObject", "request_json")

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


def request_json(*objects: dict[str, Any]) -> Union[JSONPayload, JSONObject]:
    final: dict[str, Any] = {}
    for o in objects:
        final |= o
    return orjson.dumps(final)


class NotionObject(dict[str, JSON], Generic[_KT, _VT]):
    __slots__: Sequence[str] = ()

    def __init__(self) -> None:
        super().__init__()

    def set(self, key, value) -> None:
        self[key] = value

    def nest(self, key, k: _KT, v: _VT) -> None:
        if key not in self.keys():
            self.set(key, {k: v})
        else:
            self[key] |= {k: v}  # type: ignore

    def set_array(self, key: str, values: Union[Iterable[Any], JSONObject], /) -> None:
        self[key] = list(values)
