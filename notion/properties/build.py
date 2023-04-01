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

from __future__ import annotations

from types import ModuleType
from typing import Any, Iterable, MutableMapping, Optional, Sequence, Union, cast

try:
    import orjson

    default_json: ModuleType = orjson
except ModuleNotFoundError:
    import json

    default_json: ModuleType = json

__all__: Sequence[str] = ["build_payload"]


def build_payload(
    *__obj: MutableMapping[str, Any]
) -> Union[Iterable[bytes], bytes, bytearray]:
    final: dict[str, Any] = {}
    for o in __obj:
        final.update(o)
    return cast(Union[Iterable[bytes], bytes, bytearray], default_json.dumps(final))


class NotionObject(dict[str, Any]):
    def set(self, __key: str, __val: Any) -> None:
        self[__key] = __val

    def nest(self, __Pkey: str, __Ckey: Optional[str], __val: Any) -> None:
        if __Pkey not in self:
            self.set(__Pkey, {__Ckey: __val})
        else:
            self[__Pkey].update({__Ckey: __val})

    def set_array(
        self,
        __key: str,
        values: Union[
            bytes,
            MutableMapping[str, Any],
            Sequence[Union[bytes, Any]],
        ],
    ) -> None:
        self[__key] = list(values)
