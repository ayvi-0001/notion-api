from __future__ import annotations
import os
from typing import Sequence
from typing import TypeAlias

import json
import requests

from notion.core import *
from notion.exceptions import *
from notion.api._about import *
from notion.core.typedefs import *

__all__: Sequence[str] = ["_NotionClient"]


class _NotionClient:
    """Base Class to inherit: token, headers, requests, and endpoints."""
    def __init__(self, /, *, token: str | None = None, notion_version: str | None = None):
        if token is not None:
            self.token = token
        else:
            try:
                self.token = os.getenv('NOTION_TOKEN') #type: ignore[assignment]
            except NameError: 
                pass
            finally:
                if self.token is None:
                    assert token is not None, (
                f"<{self.__class__.__name__}> Missing Token",
                "Check if dotenv is configured and token is named 'NOTION_TOKEN'")
        
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
    def _workspace_endpoint(*, users: bool = False, search: bool | None = None,
                            user_id: str | None = None, me: bool | None = None) -> NotionEndpoint:
        _search = 'search' if search else '' # search not yet implemented in subclasses
        _users = 'users' if users else ''
        _user_id = f'/{user_id}' if user_id else ''
        _me = '/me' if me else ''
        
        return f"{__base_url__}{_search}{_users}{_user_id}{_me}"

    @staticmethod
    def _block_endpoint(object_id: str | None = None, /, 
                        *, children: bool | None = None) -> NotionEndpoint:
        _object_id = f'/{object_id}' if object_id else ''
        _children = '/children' if children else ''
        
        return f"{__base_url__}blocks{_object_id}{_children}"

    @staticmethod
    def _database_endpoint(object_id: str | None = None, /, 
                           *, query: bool = False) -> NotionEndpoint:
        _object_id = f'/{object_id}' if object_id else ''
        _query = '/query' if query else ''

        return f"{__base_url__}databases{_object_id}{_query}"

    @staticmethod
    def _pages_endpoint(object_id: str | None = None, /, *, properties: bool = False, 
                        property_id: str | None = None,) -> NotionEndpoint:
        _object_id = f'/{object_id}' if object_id else ''
        _properties = '/properties' if properties else ''
        _property_id = f'/{property_id}' if property_id else ''
        
        return f"{__base_url__}pages{_object_id}{_properties}{_property_id}"


    def _get(self, url: NotionEndpoint, /, 
             *, payload: JSONObject | JSONPayload | None = None) -> JSONObject:
        if payload is None:
            response = requests.get(url, headers=self.headers)
        else:
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            response = requests.post(url, headers=self.headers, json=payload)
        
        content = json.loads(response.text)
        validate_response(content)
        return content

    def _post(self, url: NotionEndpoint, /, 
              *, payload: JSONObject | JSONPayload | None = None) -> JSONObject:
        if payload is None:
            response = requests.post(url, headers=self.headers)
        else:
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            response = requests.post(url, headers=self.headers, data=payload)
        
        content = json.loads(response.text)
        validate_response(content)
        return content

    def _patch(self, url: NotionEndpoint, /, 
               *, payload: JSONObject | JSONPayload) -> JSONObject:
        if isinstance(payload, dict):
            payload = json.dumps(payload)
        response = requests.patch(url, headers=self.headers, data=payload)
        
        content = json.loads(response.text)
        validate_response(content)
        return content

    def _delete(self, url: NotionEndpoint, /) -> JSONObject:
        response = requests.delete(url, headers=self.headers)
        
        content = json.loads(response.text)
        validate_response(content)
        return content
