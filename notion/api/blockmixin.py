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

import os
from datetime import datetime, tzinfo
from functools import cached_property
from typing import Any, MutableMapping, Optional, Sequence, Union, cast

from pytz import timezone
from tzlocal import get_localzone_name

from notion.api._about import *
from notion.api.client import _NotionClient

LOCAL_TIMEZONE = get_localzone_name()


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
    ) -> None:
        super().__init__(token=token)

        self.id: str = id.replace("-", "")

        try:
            self.tz = timezone(os.environ["TZ"])
        except KeyError:
            self.tz = timezone(LOCAL_TIMEZONE)

    def __repr__(self) -> str:
        id = getattr(self, "id", "")
        # This is to avoid certain errors occuring
        # before the object is fully initialized
        return f"notion.{self.__class__.__name__}('{id}')"

    def set_tz(self, tz: Union[tzinfo, str]) -> None:
        """
        :param tz: (required) Set the instance timezone. Takes either str or pytz.timezone\
                    Use `pytz.all_timezones()` to retrieve list of tz options.\
                    Class will first check for environment variable `TZ`.\
                    If not found, class default checks the system-configured timezone.
        """
        if isinstance(tz, tzinfo):
            self.__setattr__("tz", tz)
        elif isinstance(tz, str):
            self.__setattr__("tz", timezone(tz))

    @cached_property
    def _block(self) -> MutableMapping[str, Any]:
        """
        Same result as retrieve() for notion.api.notionblock.Block.
        If used with notion.api.notionpage.Page or notion.api.notiondatabase.Database,
        retrieves the page or database object from the blocks endpoint.

        https://developers.notion.com/reference/block#block-type-objects
        """
        return self._get(self._block_endpoint(self.id))

    @property
    def type(self) -> str:
        return cast(str, self._block["type"])

    @property
    def object(self) -> str:
        return cast(str, (self._block["object"]))

    @property
    def has_children(self) -> bool:
        return cast(bool, self._block["has_children"])

    @property
    def is_archived(self) -> bool:
        return cast(bool, self._block["archived"])

    @property
    def parent_type(self) -> str:
        ptype = cast(str, self._block["parent"]["type"])
        if "workspace" in ptype:
            return "workspace"
        return ptype

    @property
    def parent_id(self) -> str:
        _parent_id = self._block["parent"][self.parent_type]
        if _parent_id is True:  # parent is workspace
            workspace = self._get("%s%s" % (__base_url__, "users/me"))
            # return workspace name
            return "workspace-%s" % workspace["bot"]["workspace_name"]
        else:
            return cast(str, _parent_id.replace("-", ""))

    @property
    def last_edited_time(self) -> datetime:
        """
        Returns date and time when this page/block/database was created.
        Converted from ISO 8601, UTC to instance timezone.
        Class will first check for environment variable `TZ`.
        If not found, class default checks the system-configured timezone.
        Change default timezone with method `set_tz(...)`
        """
        dt = datetime.fromisoformat(self._block["last_edited_time"])
        return dt.astimezone(tz=self.tz)

    @property
    def created_time(self) -> datetime:
        """
        Returns date and time when this page/block/database was created.
        Converted from ISO 8601, UTC to instance timezone.
        Class will first check for environment variable `TZ`.
        If not found, class default checks the system-configured timezone.
        Change default timezone with method `set_tz(...)`
        """
        dt = datetime.fromisoformat(self._block["created_time"])
        return dt.astimezone(tz=self.tz)

    @property
    def last_edited_by(self) -> str:
        user_id = self._block["last_edited_by"]["id"]
        user = self._get("%s%s" % (__base_url__, "users/%s" % user_id))
        return cast(str, user)

    @property
    def created_by(self) -> str:
        user_id = self._block["created_by"]["id"]
        user = self._get("%s%s" % (__base_url__, "users/%s" % user_id))
        return cast(str, user)
