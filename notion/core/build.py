# MIT License

# Copyright (c) 2023 ayvi#0001

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

from typing import Union
from typing import Generic
from typing import Sequence
from typing import TypeVar
from typing import Iterable
from typing import Any

import orjson

from notion.core.typedefs import *

__all__: Sequence[str] = ("NotionObject", "build_payload")

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")


def build_payload(*objects: dict[str, Any]) -> JSONPayload:
    final: dict[str, Any] = {}
    for o in objects:
        final |= o
    return orjson.dumps(final)


class NotionObject(dict[str, Any], Generic[_KT, _VT]):
    __slots__: Sequence[str] = ()

    def __init__(self) -> None:
        super().__init__()

    def set(self, k: str, v: Any) -> None:
        self[k] = v

    def nest(self, key, k: _KT, v: _VT) -> None:
        if key not in self:
            self.set(key, {k: v})
        else:
            self[key] |= {k: v}

    def set_array(self, key: str, values: Union[Iterable[Any], JSONObject]) -> None:
        self[key] = list(values)
