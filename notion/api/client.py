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

# mypy: disable-error-code="no-redef"

from __future__ import annotations

import json
import logging
import os
from typing import Any, MutableMapping, Optional, Sequence

import requests

from notion.api._about import __base_url__, __content_type__
from notion.exceptions import NotionUnauthorized, validate_response

__all__: Sequence[str] = ("_NotionClient", "_NLOG")

logging.basicConfig(level=logging.INFO)

_NLOG = logging.getLogger("notion-api")


class _NotionClient:
    """Base Class to inherit: token, headers, requests, and endpoints."""

    def __init__(self, *, token: Optional[str] = None) -> None:
        if token:
            self.token = token
        else:
            try:
                self.token = os.environ["NOTION_TOKEN"]
            except KeyError:
                raise NotionUnauthorized(
                    f"notion.{self.__class__.__name__}(): Missing Token. "
                    "Check if `NOTION_TOKEN` is set in environment variables"
                )

        try:
            __notion_version__ = os.environ["NOTION_VERSION"]
        except KeyError:
            from notion.api._about import __notion_version__

        __auth__ = f"Bearer {self.token}"

        self.headers: dict[str, str] = {
            "Authorization": __auth__,
            "Accept": __content_type__,
            "Content-type": __content_type__,
            "Notion-Version": __notion_version__,
        }

    @staticmethod
    def _block_endpoint(
        block_id: Optional[str] = None,
        /,
        *,
        children: Optional[bool] = False,
        page_size: Optional[int] = None,
        start_cursor: Optional[str] = None,
    ) -> str:
        return "".join(
            [
                __base_url__,
                "blocks",
                f"/{block_id}" if block_id else "",
                "/children" if children else "",
                "?" if any([page_size, start_cursor]) else "",
                f"&start_cursor={start_cursor}" if start_cursor else "",
                f"&page_size={page_size}" if page_size else "",
            ]
        )

    @staticmethod
    def _database_endpoint(
        database_id: Optional[str] = None, /, *, query: Optional[bool] = False
    ) -> str:
        return "".join(
            [
                __base_url__,
                "databases",
                f"/{database_id}" if database_id else "",
                "/query" if query else "",
            ]
        )

    @staticmethod
    def _pages_endpoint(
        page_id: Optional[str] = None,
        /,
        *,
        properties: Optional[bool] = False,
        property_id: Optional[str] = None,
    ) -> str:
        return "".join(
            [
                __base_url__,
                "pages",
                f"/{page_id}" if page_id else "",
                "/properties" if properties else "",
                f"/{property_id}" if property_id else "",
            ]
        )

    @staticmethod
    def _users_endpoint(
        user_id: Optional[str] = None,
        /,
        me: bool = False,
    ) -> str:
        return "".join(
            [
                __base_url__,
                "users",
                f"/{user_id}",
                f"/me" if me else "",
            ]
        )

    def _get(
        self,
        url: str,
        payload: Optional[MutableMapping[str, Any] | str | bytes] = None,
    ) -> MutableMapping[str, Any]:
        if not payload:
            request = requests.get(url, headers=self.headers).text
            response = validate_response(request)
        else:
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            request = requests.post(url, headers=self.headers, data=payload).text
            response = validate_response(request)
        return response

    def _post(
        self,
        url: str,
        payload: Optional[MutableMapping[str, Any] | str | bytes] = None,
    ) -> MutableMapping[str, Any]:
        if not payload:
            request = requests.post(url, headers=self.headers).text
            response = validate_response(request)
        else:
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            request = requests.post(url, headers=self.headers, data=payload).text
            response = validate_response(request)
        return response

    def _patch(
        self,
        url: str,
        payload: MutableMapping[str, Any] | str | bytes,
    ) -> MutableMapping[str, Any]:
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        request = requests.patch(url, headers=self.headers, data=payload).text
        response = validate_response(request)
        return response

    def _delete(self, url: str) -> MutableMapping[str, Any]:
        request = requests.delete(url, headers=self.headers).text
        response = validate_response(request)
        return response
