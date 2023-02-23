from __future__ import annotations
from functools import cached_property
from typing import Sequence
from typing import Optional
from typing import Union
from typing import Optional
from datetime import datetime
from datetime import tzinfo

from pytz import timezone 
from uuid import UUID

from notion.api._about import *
from notion.core.typedefs import *
from notion.api.client import _NotionClient
from notion.exceptions.errors import NotionObjectNotFound

__all__: Sequence[str] = ["_TokenBlockMixin"]


class _TokenBlockMixin(_NotionClient):
    """
    Any object you interact with in Notion; 
    Databases/Pages/individual child blocks, are all considered 'Blocks'
    This class assigns common attributes among all three types.
    """
    def __init__(
        self, 
        id: str, 
        /, 
        *, 
        token: Optional[str] = None, 
        notion_version: Optional[str] = None
    ) -> None:
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
    def _block(self) -> JSONObject:
        """ 
        Same result as retrieve() for `notion.api.notionblock.Block`.
        If used with `notion.api.notionpage.Page` or `notion.api.notiondatabase.Database`,
        retrieves the page or database object from the blocks endpoint.
        """
        return self._get(self._block_endpoint(self.id))

    @property
    def type(self) -> str:
        return str(self._block['type'])
    
    @property
    def object(self) -> str:
        return str(self._block['object'])

    @property
    def has_children(self) -> bool:
        return bool(self._block['has_children'])

    @property
    def is_archived(self) -> bool:
        return bool(self._block['archived'])
    
    @property
    def parent_type(self) -> str:
        return str(self._block['parent']['type'])
    
    @property
    def parent_id(self) -> str:
        _parent_id = self._block['parent'][self.parent_type]
        if _parent_id is True:
            # sets key to 'workspace' rather than 'True'
            _parent_id = self.parent_type 
        else:
            _parent_id = _parent_id.replace('-','')
        return str(_parent_id)
   
    def set_default_tz(self, timezone: Union[tzinfo, str]) -> None:
        """
        :param timezone: (required) set default timezone. class default is 'PST8PDT' \
            Use `pytz.all_timezones` to retrieve list of tz options. \
            Pass either str or `pytz.timezone(...)`
        """
        self.__setattr__('default_tz', timezone)

    @property
    def last_edited(self) -> datetime:
        """ 
        Notion returns datetime ISO 8601, UTC. 
        Class uses UTC-8:00 ('PST8PDT') as default.
        Change default timezone with `set_default_tz(...)`
        """
        last_edited_time = self._block['last_edited_time']
        dt = datetime.fromisoformat(last_edited_time)
        return dt.astimezone(tz=timezone(self.default_tz)) 

    @property
    def created(self) -> datetime:
        """ 
        Notion returns datetime ISO 8601, UTC. 
        Class uses UTC-8:00 ('PST8PDT') as default.
        Change default timezone with `set_default_tz(...)`
        """
        created_time = self._block['created_time']
        dt = datetime.fromisoformat(created_time)
        return dt.astimezone(tz=timezone(self.default_tz)) 

    def __repr__(self) -> str:
        return f"notion.{self.__class__.__name__}('{self.id}')"
