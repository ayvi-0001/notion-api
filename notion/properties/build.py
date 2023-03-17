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

from types import ModuleType
from typing import Any, Iterable, MutableMapping, Optional, Sequence, Union

try:
    import orjson

    default_json: ModuleType = orjson
except ModuleNotFoundError:
    import json

    default_json: ModuleType = json  # type: ignore[no-redef]

__all__: Sequence[str] = ["build_payload"]


def build_payload(*objects: dict[str, Any]) -> Union[Iterable[bytes], bytes, bytearray]:
    final: dict[str, Any] = {}
    for o in objects:
        final |= o
    return default_json.dumps(final)  # type: ignore[no-any-return]


class NotionObject(dict[str, Any]):
    __slots__: Sequence[str] = ()

    def __init__(self) -> None:
        super().__init__()

    def set(self, k: str, v: Any) -> None:
        self[k] = v

    def nest(self, key: str, k: Optional[str], v: Any) -> None:
        if key not in self:
            self.set(key, {k: v})
        else:
            self[key] |= {k: v}

    def set_array(
        self,
        key: str,
        values: Union[
            Iterable[bytes],
            bytes,
            bytearray,
            MutableMapping[str, Any],
            Sequence[Any],
        ],
    ) -> None:
        self[key] = list(values)
