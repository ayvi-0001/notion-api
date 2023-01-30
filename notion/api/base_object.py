from __future__ import annotations

from functools import cached_property
from typing import Sequence
from typing import Optional
from datetime import datetime
from datetime import tzinfo

from uuid import UUID
from pytz import timezone # type: ignore[import]
# Occasional issues with downloading library stubs for pytz
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
    def block_endpoint(self) -> JSONObject:
        """Returns the object 'Block' for the Block, Page, or Database."""
        url = super()._endpoint('blocks', object_id=self.id)
        return super()._get(url)
    
    @property
    def type(self) -> JSONObject:
        return self.block_endpoint['type']
    
    @property
    def object(self) -> JSONObject:
        return self.block_endpoint['object']

    @property
    def has_children(self) -> JSONObject:
        return self.block_endpoint['has_children']

    @property
    def is_archived(self) -> JSONObject:
        return self.block_endpoint['archived']
    
    @property
    def parent_type(self) -> JSONObject:
        response = self.block_endpoint['parent'].get('type')
        return response

    @property
    def parent_id(self) -> JSONObject:
        _parent_id = self.block_endpoint['parent'].get(self.parent_type)
        if _parent_id is True:
            _parent_id = self.parent_type # set key to 'workspace' rather than 'True'
        else:
            _parent_id = _parent_id.replace('-','')
        return _parent_id

    def set_default_tz(self, timezone: Optional[tzinfo | str]):
        """ 
        (required)
        :param timez: set default timezone. class default = 'PST8PDT'
                      Use pytz.all_timezones to retrieve list of tz options.
                      Pass either string or pytz.timezone(...)
        """
        self.__setattr__('default_tz', timezone)

    @property
    def last_edited(self):
        """Notion returns datetime ISO 8601, UTC. 
        Class uses UTC-8:00 ('PST8PDT') as default.
        Change default timezone by calling set_default_tz(...)
        
        Access values with datetime attributes:
        example_block.last_edited.date
        example_block.last_edited.time
        """
        _last_edited_time = self.block_endpoint.get('last_edited_time')
        assert _last_edited_time is not None 
        _dt = datetime.fromisoformat(
            _last_edited_time).astimezone(tz=timezone(self.default_tz)) 

        @dataclass(frozen=True)
        class LastEditedTime:
            date = _dt.strftime("%m/%d/%Y")
            day = _dt.strftime("%d")
            month = _dt.strftime("%m")
            year = _dt.strftime("%Y")
            time = _dt.strftime("%H:%M:%S")

        return LastEditedTime()

    @property
    def created(self):
        """Notion returns datetime ISO 8601, UTC. 
        Class uses UTC-8:00 ('PST8PDT') as default.
        Change default timezone by calling set_default_tz(...)
        
        Access values with datetime attributes:
        example_block.created.date
        example_block.created.time
        """
        _created_time = self.block_endpoint.get('created_time')
        assert _created_time is not None 
        _dt = datetime.fromisoformat(
            _created_time).astimezone(tz=timezone(self.default_tz)) 

        @dataclass(frozen=True)
        class CreatedTime:
            date = _dt.strftime("%m/%d/%Y")
            day = _dt.strftime("%d")
            month = _dt.strftime("%m")
            year = _dt.strftime("%Y")
            time = _dt.strftime("%H:%M:%S")

        return CreatedTime()

    def __repr__(self):
        return f'<{self.__class__.__name__.lower()}_{self.id}>'
