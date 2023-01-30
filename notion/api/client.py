from __future__ import annotations
import os
from typing import Sequence
from typing import Literal
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
            
        self.headers: dict[str, str] = {
            "Authorization": f'Bearer {self.token}',
            "Content-type": __content_type__,
            "Notion-Version": __notion_version__,
        }

        if notion_version is not None:
            self.headers['Notion-Version'] = notion_version
        

    NotionEndpoint: TypeAlias = str
    @staticmethod
    def _endpoint(type: Literal['blocks', 'databases', 'pages'], /, 
                  *,
                  object_id: str | None = None, 
                  children: bool = False, 
                  properties: bool = False,
                  property_id: str | None = None,
                  query: bool = False
        ) -> NotionEndpoint:

        object_id_ = '' if object_id is None else f'/{object_id}'
        children_ = '' if children is False else '/children'
        properties_ = '' if properties is False else '/properties'
        property_id_ = '' if property_id is None else f'/{property_id}'
        query_ = '' if query is False else '/query'
        
        return f"{__base_url__}{type}{object_id_}{children_}{properties_}{property_id_}{query_}"

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
