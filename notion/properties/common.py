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

from typing import Any, Optional, Sequence

from notion.properties.build import NotionObject

__all__: Sequence[str] = (
    "Parent",
    "UserObject",
    "BotObject",
    "_NotionUUID",
    "_NotionURL",
)


class Parent(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, parent_id: str, /, *, type: str) -> None:
        """
        Pages, databases, and blocks are either located inside other pages, databases, and blocks,
        or are located at the top level of a workspace. This location is known as the "parent".
        Parent information is represented by a consistent parent object throughout the API.

        Parenting rules:
         - Pages can be parented by other pages, databases, blocks, or by the whole workspace.
         - Blocks can be parented by pages, databases, or blocks.
         - Databases can be parented by pages, blocks, or by the whole workspace.

        A page with a workspace parent is a top-level page within a Notion workspace.
        https://developers.notion.com/reference/parent-object#workspace-parent
        Cannot create pages/databases at the top-level via the API.

        https://developers.notion.com/reference/parent-object
        """
        super().__init__()
        self.nest("parent", "type", type)
        self.nest("parent", type, parent_id)

    @classmethod
    def page(cls, parent_id: str, /) -> Parent:
        """https://developers.notion.com/reference/parent-object#page-parent"""
        return cls(parent_id, type="page_id")

    @classmethod
    def database(cls, parent_id: str, /) -> Parent:
        """https://developers.notion.com/reference/parent-object#database-parent"""
        return cls(parent_id, type="database_id")

    @classmethod
    def block(cls, parent_id: str, /) -> Parent:
        """
        A page may have a block parent if it is created inline in a chunk of text,
        or is located beneath another block like a toggle or bullet block.

        https://developers.notion.com/reference/parent-object#block-parent
        """
        return cls(parent_id, type="block_id")


class UserObject(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        id: str,
        name: Optional[str] = None,
        avatar_url: Optional[str] = None,
        email: Optional[str] = None,
    ) -> None:
        """
        The User object represents a user in a Notion workspace. Users include full workspace members, and integrations.
        Guests are not included.

        ---
        :param id: (required) Unique identifier for this user. *Always present
        :param name: (optional) User's name, as displayed in Notion.
        :param avatar_url: (optional)
        :param email: (optional)

        ---
        User objects appear in the API in nearly all objects returned by the API, including:
            - Block object under created_by and last_edited_by.
            - Page object under created_by and last_edited_by and in people property items.
            - Database object under created_by and last_edited_by.
            - Rich text object, as user mentions.
            - Property object when the property is a people property.

        User objects will always contain object and id keys.
        The remaining properties may appear if the user is being rendered in a rich text or
        page property context, and the bot has the correct capabilities to access those properties.

        If your integration doesn't yet have access to the mentioned user,
        then the plain_text that would include a user's name reads as "@Anonymous".
        To update the integration to get access to the user,
        update the integration capabilities on the integration settings page.

        All parameters are display-only and cannot be updated.

        https://developers.notion.com/reference/user
        """
        super().__init__()
        self.set("object", "user")
        self.set("id", id)
        self.set("name", name) if name else None
        self.set("avatar_url", avatar_url) if avatar_url else None
        self.set("type", "person")
        if email:
            self.nest("person", "email", email)
        else:
            self.set("person", {})


class BotObject(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        id: str,
        workspace_name: Optional[str] = None,
        name: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> None:
        """https://developers.notion.com/reference/user#bots"""
        super().__init__()
        self.set("object", "user")
        self.set("id", id)
        self.set("name", name) if name else None
        self.set("avatar_url", avatar_url) if avatar_url else None
        self.set("type", "bot")
        self.nest("bot", "owner", {"type": "workspace", "workspace": True})
        self.nest("bot", "workspace_name", workspace_name)


class _NotionURL(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, url: str, /) -> None:
        """Internal object for URL properties."""
        super().__init__()
        self.set("url", url)


class _NotionUUID(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, id: str, /) -> None:
        """Internal object for UUID properties."""
        super().__init__()
        self.set("id", id)
