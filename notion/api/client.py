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

import logging
import os
from types import ModuleType
from typing import Any, Iterable, MutableMapping, Optional, Sequence, Union, cast

try:
    import orjson

    default_json: ModuleType = orjson
except ModuleNotFoundError:
    import json

    default_json: ModuleType = json

import requests

from notion.api._about import *
from notion.exceptions import NotionUnauthorized, validate_response

__all__: Sequence[str] = ["_NotionClient"]

logging.basicConfig(level=logging.INFO)

_NLOG = logging.getLogger("notion-api")


class _NotionClient:
    """Base Class to inherit: token, headers, requests, and endpoints."""

    def __init__(
        self, *, token: Optional[str] = None, notion_version: Optional[str] = None
    ) -> None:
        if token:
            self.token = token
        else:
            try:
                self.token = os.environ["NOTION_TOKEN"]
            except KeyError:
                if not token:
                    raise NotionUnauthorized(
                        "%s. %s."
                        % (
                            f"notion.{self.__class__.__name__}: Missing Token",
                            "Check if `NOTION_TOKEN` is set in environment variables",
                        )
                    )

        __auth__ = f"Bearer {self.token}"

        self.headers: dict[str, str] = {
            "Authorization": __auth__,
            "Accept": __content_type__,
            "Content-type": __content_type__,
            "Notion-Version": __notion_version__,
        }

        if notion_version:
            self.headers["Notion-Version"] = notion_version

    @staticmethod
    def _block_endpoint(
        object_id: Optional[str] = None,
        /,
        *,
        children: Optional[bool] = None,
        page_size: Optional[int] = None,
        start_cursor: Optional[str] = None,
    ) -> str:
        return "%sblocks%s%s%s%s%s" % (
            __base_url__,
            f"/{object_id}" if object_id else "",
            "/children" if children else "",
            "?" if any([page_size, start_cursor]) else "",
            f"&start_cursor={start_cursor}" if start_cursor else "",
            f"&page_size={page_size}" if page_size else "",
        )

    @staticmethod
    def _database_endpoint(
        object_id: Optional[str] = None, /, *, query: Optional[bool] = False
    ) -> str:
        return "%sdatabases%s%s" % (
            __base_url__,
            f"/{object_id}" if object_id else "",
            "/query" if query else "",
        )

    @staticmethod
    def _pages_endpoint(
        object_id: Optional[str] = None,
        /,
        *,
        properties: Optional[bool] = False,
        property_id: Optional[str] = None,
    ) -> str:
        return "%spages%s%s%s" % (
            __base_url__,
            f"/{object_id}" if object_id else "",
            "/properties" if properties else "",
            f"/{property_id}" if property_id else "",
        )

    def _get(
        self,
        url: str,
        /,
        *,
        payload: Optional[
            Union[MutableMapping[str, Any], Union[bytes, Iterable[bytes]]]
        ] = None,
    ) -> MutableMapping[str, Any]:
        if not payload:
            response = default_json.loads(requests.get(url, headers=self.headers).text)
        else:
            if isinstance(payload, dict):
                payload = default_json.dumps(payload)
            response = default_json.loads(
                requests.post(url, headers=self.headers, json=payload).text
            )

        validate_response(response)
        return cast(MutableMapping[str, Any], response)

    def _post(
        self,
        url: str,
        /,
        *,
        payload: Optional[
            Union[MutableMapping[str, Any], Union[bytes, Iterable[bytes]]]
        ] = None,
    ) -> MutableMapping[str, Any]:
        if not payload:
            response = default_json.loads(requests.post(url, headers=self.headers).text)
        else:
            if isinstance(payload, dict):
                payload = default_json.dumps(payload)
            response = default_json.loads(
                requests.post(url, headers=self.headers, data=payload).text
            )

        validate_response(response)
        return cast(MutableMapping[str, Any], response)

    def _patch(
        self,
        url: str,
        /,
        *,
        payload: Union[MutableMapping[str, Any], Union[bytes, Iterable[bytes]]],
    ) -> MutableMapping[str, Any]:
        if isinstance(payload, dict):
            payload = default_json.dumps(payload)
        response = default_json.loads(
            requests.patch(url, headers=self.headers, data=payload).text
        )

        validate_response(response)
        return cast(MutableMapping[str, Any], response)

    def _delete(self, url: str, /) -> MutableMapping[str, Any]:
        response = default_json.loads(requests.delete(url, headers=self.headers).text)

        validate_response(response)
        return cast(MutableMapping[str, Any], response)
