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
from typing import Any, MutableMapping, Optional, Sequence, cast

try:
    import orjson

    _json: ModuleType = orjson
except ModuleNotFoundError:
    import json

    _json: ModuleType = json  # type: ignore[no-redef]

__all__: Sequence[str] = ("build_payload",)


def build_payload(*objects: MutableMapping[str, Any]) -> str:
    final: dict[str, Any] = {}
    for o in objects:
        final.update(o)
    return cast(str | bytes, _json.dumps(final))


class NotionObject(dict[str, Any]):
    def set(self, _key: str, _val: Any) -> None:
        self[_key] = _val

    def nest(self, _Pkey: str, _Ckey: Optional[str], _val: Any) -> None:
        if _Pkey not in self:
            self.set(_Pkey, {_Ckey: _val})
        else:
            self[_Pkey].update({_Ckey: _val})

    def set_array(
        self, _key: str, values: bytes | MutableMapping[str, Any] | Sequence[bytes | Any]
    ) -> None:
        self[_key] = list(values)
