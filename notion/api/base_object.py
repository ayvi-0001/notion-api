from __future__ import annotations

from functools import cached_property
from typing import Sequence
from typing import Optional
from typing import Any
from datetime import datetime
from datetime import tzinfo

from uuid import UUID
from pytz import timezone # type: ignore[import]
from pydantic.dataclasses import dataclass

from notion.api._about import *
from notion.api.client import *
from notion.exceptions import *
from notion.core.typedefs import *

__all__: Sequence[str] = ["_BaseNotionBlock"]


class _BaseNotionBlock(_NotionClient):
    """All objects you interact with in Notion are considered 'Blocks'; 
    Databases, Pages, or the individual child blocks in a page. 

    Class assigns basic attributes common among all three types.

    The current version of Notion's API does not allow creating
    objects at the workspace level, and require a parent id.
    Subclasses use this for validation.
    """
    def __init__(self, id: str, /, *, token: str | None = None, notion_version: str | None = None):
        super().__init__(token=token, notion_version=notion_version)

        self.default_tz = __default_timezone__
        self.id = id.replace('-','')
        
        try:
            UUID(self.id)
        except ValueError:
            __failed_instance__ = f"""
            {self.__repr__()} instatiation failed validation:
            id should be a valid uuid, instead was `'{self.id}'`
            """
            raise NotionObjectNotFound(__failed_instance__)

    @cached_property
    def as_block(self) -> JSONObject:
        """Returns the object 'Block' for the Block, Page, or Database."""
        return self._get(self._block_endpoint(self.id))
    
    @property
    def type(self) -> JSONObject:
        return self.as_block['type']
    
    @property
    def object(self) -> JSONObject:
        return self.as_block['object']

    @property
    def has_children(self) -> JSONObject:
        return self.as_block['has_children']

    @property
    def is_archived(self) -> JSONObject:
        return self.as_block['archived']
    
    @property
    def parent_type(self) -> JSONObject:
        return self.as_block['parent']['type']
    
    @property
    def url(self) -> JSONObject:
        """ URL is not available in the block object response.
        URL key shows up in page/database retrieve.
        """
        return self.as_block['url']

    @property
    def parent_id(self) -> str | Any:
        _parent_id = self.as_block['parent'][self.parent_type]
        if _parent_id is True:
            _parent_id = self.parent_type # sets key to 'workspace' rather than 'True'
        else:
            _parent_id = _parent_id.replace('-','')
        return _parent_id

    def set_default_tz(self, timezone: Optional[tzinfo | str]) -> None:
        """ 
        (required)
        :param timez: set default timezone. class default = 'PST8PDT'
                      Use pytz.all_timezones to retrieve list of tz options.
                      Pass either string or pytz.timezone(...)
        """
        self.__setattr__('default_tz', timezone)
    
    @property
    def list_all_users(self) -> JSONObject:
        """Returns a paginated list of Users for the workspace. 
        The response may contain fewer than page_size of results.
        ---
        https://developers.notion.com/reference/get-users
        """
        return self._get(self._workspace_endpoint(users=True))

    @property
    def retrieve_token_bot(self):
        """ Retrieves the bot User associated with the API token provided in the authorization header. 
        The bot will have an owner field with information about the person who authorized the integration. 
        ---
        https://developers.notion.com/reference/get-self """
        return self._get(self._workspace_endpoint(users=True, me=True))
    
    def retrieve_user(self, user_id: str) -> JSONObject:
        """Retrieves a User using the ID specified.
        (required)
        :param user_id: Identifier for a Notion user
        ---
        https://developers.notion.com/reference/get-users
        """
        return self._get(self._workspace_endpoint(users=True, user_id=user_id))

    @property
    def last_edited(self):
        """Notion returns datetime ISO 8601, UTC. 
        Class uses UTC-8:00 ('PST8PDT') as default.
        Change default timezone by calling set_default_tz(...)
        
        Access values with datetime attributes:
        example_block.last_edited.date
        example_block.last_edited.time
        """
        last_edited_time = self.as_block['last_edited_time']
        dt = datetime.fromisoformat(
            last_edited_time).astimezone(tz=timezone(self.default_tz)) 

        @dataclass(frozen=True)
        class BlockLastEditedTime:
            date = dt.strftime("%m/%d/%Y")
            day = dt.strftime("%d")
            month = dt.strftime("%m")
            year = dt.strftime("%Y")
            time = dt.strftime("%H:%M:%S")

        return BlockLastEditedTime()

    @property
    def created(self):
        """Notion returns datetime ISO 8601, UTC. 
        Class uses UTC-8:00 ('PST8PDT') as default.
        Change default timezone by calling set_default_tz(...)
        
        Access values with datetime attributes:
        example_block.created.date
        example_block.created.time
        """
        created_time = self.as_block['created_time']
        dt = datetime.fromisoformat(
            created_time).astimezone(tz=timezone(self.default_tz)) 

        @dataclass(frozen=True)
        class BlockCreatedTime:
            date = dt.strftime("%m/%d/%Y")
            day = dt.strftime("%d")
            month = dt.strftime("%m")
            year = dt.strftime("%Y")
            time = dt.strftime("%H:%M:%S")

        return BlockCreatedTime()

    def __repr__(self) -> str:
        return f"<notion.{self.__class__.__name__}('{self.id}')'>"
