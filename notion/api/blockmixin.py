from __future__ import annotations

from functools import cached_property
from typing import Sequence
from typing import Optional
from datetime import datetime
from datetime import tzinfo

from uuid import UUID
from pytz import timezone 
from dataclasses import dataclass

from notion.api._about import *
from notion.core.typedefs import *
from notion.api.client import _NotionClient
from notion.exceptions import NotionObjectNotFound

__all__: Sequence[str] = ["_TokenBlockMixin"]


class _TokenBlockMixin(_NotionClient):
    """Any object you interact with in Notion; Databases/Pages/individual child blocks, are all considered 'Blocks'
    This class assigns common attributes among all three types.
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
                id should be a valid uuid, instead was `'{self.id}'`"""
            raise NotionObjectNotFound(__failed_instance__)

    @cached_property
    def __block__(self) -> JSONObject:
        """ If used on `notion.api.notionblock.Block`, the result is the same as retrieve() method.
        If used on `notion.api.notionpage.Page` or `notion.api.notiondatabase.Database`,
        retrieves the page or database object from the blocks endpoint.
        """
        return self._get(self._block_endpoint(self.id))

    @property
    def type(self) -> JSONObject:
        return self.__block__['type']
    
    @property
    def object(self) -> JSONObject:
        return self.__block__['object']

    @property
    def has_children(self) -> JSONObject:
        return self.__block__['has_children']

    @property
    def is_archived(self) -> JSONObject:
        return self.__block__['archived']
    
    @property
    def parent_type(self) -> JSONObject:
        return self.__block__['parent']['type']
    
    @property
    def parent_id(self) -> str:
        _parent_id = self.__block__['parent'][self.parent_type]
        if _parent_id is True:
            # sets key to 'workspace' rather than 'True'
            _parent_id = self.parent_type 
        else:
            _parent_id = _parent_id.replace('-','')
        return str(_parent_id)
   
    def set_default_tz(self, timezone: Optional[tzinfo | str]) -> None:
        """
        :param timezone: (required) set default timezone. class default is 'PST8PDT' \
            Use `pytz.all_timezones` to retrieve list of tz options. Pass either string or `pytz.timezone(...)`
        """
        self.__setattr__('default_tz', timezone)

    @property
    def last_edited(self):
        """ Notion returns datetime ISO 8601, UTC. Class uses UTC-8:00 ('PST8PDT') as default.
        Change default timezone with `set_default_tz(...)`

        Access values with datetime attributes:
        example_block.last_edited.date
        example_block.last_edited.time
        """
        last_edited_time = self.__block__['last_edited_time']
        dtiso = datetime.fromisoformat(last_edited_time)
        dtz = dtiso.astimezone(tz=timezone(self.default_tz)) 

        @dataclass(frozen=True, slots=True, init=False)
        class LastEditedTime:
            date = dtz.strftime("%m/%d/%Y")
            day = dtz.strftime("%d")
            month = dtz.strftime("%m")
            year = dtz.strftime("%Y")
            time = dtz.strftime("%H:%M:%S")

        return LastEditedTime()

    @property
    def created(self):
        """ Notion returns datetime ISO 8601, UTC. Class uses UTC-8:00 ('PST8PDT') as default.
        Change default timezone with `set_default_tz(...)`
        
        Access values with datetime attributes:
        example_block.created.date
        example_block.created.time
        """
        created_time = self.__block__['created_time']
        dtiso = datetime.fromisoformat(created_time)
        dtz = dtiso.astimezone(tz=timezone(self.default_tz)) 

        @dataclass(frozen=True, slots=True, init=False)
        class CreatedTime:
            date = dtz.strftime("%m/%d/%Y")
            day = dtz.strftime("%d")
            month = dtz.strftime("%m")
            year = dtz.strftime("%Y")
            time = dtz.strftime("%H:%M:%S")

        return CreatedTime()

    def __repr__(self) -> str:
        return f"notion.{self.__class__.__name__}('{self.id}')"
