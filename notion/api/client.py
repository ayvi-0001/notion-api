from __future__ import annotations
import os
from typing import Sequence
from typing import TypeAlias

import requests
import orjson

from notion.core import *
from notion.exceptions import *
from notion.api._about import *
from notion.core.typedefs import *

__all__: Sequence[str] = ["_NotionClient"]


class _NotionClient:
    """Base Class to inherit: token, headers, requests, and endpoints."""
    def __init__(self, /, *, token: str | None = None, notion_version: str | None = None):
        if token:
            self.token = token
        else:
            try:
                self.token = os.getenv('NOTION_TOKEN')
            except NameError: 
                pass
            finally:
                if self.token is None:
                    raise NotionUnauthorized(
                        f"notion.{self.__class__.__name__} {__token_error__}")
        
        __auth__ = f'Bearer {self.token}'
            
        self.headers: dict[str, str] = {
            "Authorization": __auth__,
            "Content-type": __content_type__,
            "Notion-Version": __notion_version__,
            }

        if notion_version is not None:
            self.headers['Notion-Version'] = notion_version
        

    NotionEndpoint: TypeAlias = str
    @staticmethod
    def _block_endpoint(object_id: str | None = None, 
                        /, *, 
                        children: bool | None = None,
                        page_size: int | None = None,
                        start_cursor: str | None = None) -> NotionEndpoint:

        _object_id = f'/{object_id}' if object_id else ''
        _children = '/children' if children else ''

        urlparam = ''
        if any([page_size, start_cursor]):
            urlparam = '?'
        _page_size = f'&page_size={page_size}' if page_size else ''
        _start_cursor = f'&start_cursor={start_cursor}' if start_cursor else ''
        
        return f"{__base_url__}blocks{_object_id}{_children}{urlparam}{_start_cursor}{_page_size}"

    @staticmethod
    def _database_endpoint(object_id: str | None = None, /, *, 
                           query: bool = False) -> NotionEndpoint:

        _object_id = f'/{object_id}' if object_id else ''
        _query = '/query' if query else ''

        return f"{__base_url__}databases{_object_id}{_query}"

    @staticmethod
    def _pages_endpoint(object_id: str | None = None, /, *, 
                        properties: bool = False, property_id: str | None = None
                        ) -> NotionEndpoint:

        _object_id = f'/{object_id}' if object_id else ''
        _properties = '/properties' if properties else ''
        _property_id = f'/{property_id}' if property_id else ''
        
        return f"{__base_url__}pages{_object_id}{_properties}{_property_id}"


    def _get(self, url: NotionEndpoint, /, *, 
             payload: JSONObject | JSONPayload | None = None) -> JSONObject:
        if payload is None:
            response = orjson.loads(requests.get(url, headers=self.headers).text)
        else:
            if isinstance(payload, dict):
                payload = orjson.dumps(payload)
            response = orjson.loads(
                requests.post(url, headers=self.headers, json=payload).text)
        
        validate_response(response)
        return response

    def _post(self, url: NotionEndpoint, /, *, 
              payload: JSONObject | JSONPayload | None = None) -> JSONObject:
        if payload is None:
            response = orjson.loads(requests.post(url, headers=self.headers).text)
        else:
            if isinstance(payload, dict):
                payload = orjson.dumps(payload)
            response = orjson.loads(
                requests.post(url, headers=self.headers, data=payload).text)

        validate_response(response)
        return response

    def _patch(self, url: NotionEndpoint, /, *, 
               payload: JSONObject | JSONPayload) -> JSONObject:
        if isinstance(payload, dict):
            payload = orjson.dumps(payload)
        response = orjson.loads(
            requests.patch(url, headers=self.headers, data=payload).text)

        validate_response(response)
        return response

    def _delete(self, url: NotionEndpoint, /) -> JSONObject:
        response = orjson.loads(requests.delete(url, headers=self.headers).text)

        validate_response(response)
        return response
