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

from functools import partial, partialmethod
from typing import Any, Callable, MutableMapping, Optional, Sequence, TypeVar

__all__ = ("paginated_response_endpoint", "paginated_response_payload")


T = TypeVar("T", covariant=True)


def paginated_response_endpoint(
    call: partialmethod[MutableMapping[str, Sequence[T]]],
    endpoint: partial[str],
    max_page_size: Optional[int] = None,
) -> list[T]:
    results: list[T] = []

    def append_results(request: MutableMapping[str, Sequence[T]]) -> list[T]:
        for result in request["results"]:
            if max_page_size is not None and len(results) >= max_page_size:
                return results
            results.append(result)

        if "next_cursor" in request and request["has_more"]:
            return append_results(
                call.func(
                    endpoint(start_cursor=request["next_cursor"], page_size=max_page_size)
                )
            )
        return results

    append_results(call.func(endpoint()))
    return results


def paginated_response_payload(
    call: Callable[[str], MutableMapping[str, Sequence[T]]],
    endpoint: str,
    payload: dict[str, Any],
    max_page_size: Optional[int] = None,
) -> list[T]:
    results: list[T] = []
    request = partial(call, endpoint)

    def append_results(response: MutableMapping[str, Sequence[T]]) -> list[T]:
        for result in response["results"]:
            if max_page_size is not None and len(results) >= max_page_size:
                return results
            results.append(result)

        if "next_cursor" in response and response["has_more"]:
            payload["start_cursor"] = response["next_cursor"]
            return append_results(request(payload))

        return results

    append_results(request(payload))
    return results
