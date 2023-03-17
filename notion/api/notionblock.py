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

from functools import cached_property
from typing import Any, Iterable, MutableMapping, Optional, Sequence, Union

from notion.api.blockmixin import _TokenBlockMixin
from notion.api.client import _NLOG

__all__: Sequence[str] = ["Block"]


class Block(_TokenBlockMixin):
    """A block object represents content within Notion.
    Blocks can be text, lists, media, and more. A page is a type of block, too.

    These are the individual 'nodes' in a page that you typically interact with in Notion.
    Some blocks have more content nested inside them.
    Some examples are indented paragraphs, lists, and toggles.
    The nested content is called children, and children are blocks, too.

    ---
    :param id: (required) `block_id` of object in Notion.
    :param token: (required) Bearer token provided when you create an integration.
        set as `NOTION_TOKEN` in .env or set variable here.
        see https://developers.notion.com/reference/authentication.
    :param notion_version: (optional) API version
        see https://developers.notion.com/reference/versioning

    https://developers.notion.com/reference/block
    """

    def __init__(
        self,
        id: str,
        /,
        *,
        token: Optional[str] = None,
        notion_version: Optional[str] = None,
    ) -> None:
        super().__init__(id, token=token, notion_version=notion_version)

        self.logger = _NLOG.getChild(f"{self.__repr__()}")

    @cached_property
    def retrieve(self) -> MutableMapping[str, Any]:
        """
        Retrieves a Block object using the ID specified.

        https://developers.notion.com/reference/retrieve-a-block
        """
        return self._get(self._block_endpoint(self.id))

    def retrieve_children(
        self, start_cursor: Optional[str] = None, page_size: Optional[int] = None
    ) -> MutableMapping[str, Any]:
        """
        Returns a paginated array of child block objects contained
        in the block using the ID specified.

        Returns only the first level of children for the specified block.
        See block objects for more detail on determining if that block has nested children.
        In order to receive a complete representation of a block,
        you may need to recursively retrieve block children of child blocks.
        page_size Default: 100 page_size Maximum: 100.

        https://developers.notion.com/reference/get-block-children
        """
        return self._get(
            self._block_endpoint(
                self.id, children=True, page_size=page_size, start_cursor=start_cursor
            )
        )

    def _append(
        self,
        payload: Union[
            MutableMapping[str, Any], Union[Iterable[bytes], bytes, bytearray]
        ],
    ) -> MutableMapping[str, Any]:
        """
        Creates/appends new children blocks to the parent block_id specified.
        Returns a paginated list of newly created children block objects.

        Used internally by `notion.api.blocktypefactory.BlockFactory`.

        https://developers.notion.com/reference/patch-block-children
        """
        return self._patch(
            self._block_endpoint(self.id, children=True), payload=payload
        )

    @property
    def delete_self(self) -> None:
        """
        Sets a Block object, including page blocks, to archived: true
        using the ID specified. Note: in the Notion UI application,
        this moves the block to the "Trash" where it can still be
        accessed and restored. To restore the block with the API,
        use the Update a block or Update page respectively.

        https://developers.notion.com/reference/delete-a-block
        """
        self._delete(self._block_endpoint(self.id))
        self.logger.info("Deleted Self.")

    @property
    def restore_self(self) -> None:
        """
        Sets "archived" key to false.
        Only works if the parent page has not been deleted from the trash.
        """
        self._patch(self._block_endpoint(self.id), payload=(b'{"archived": false}'))
        self.logger.info("Restored Self.")

    def delete_child(self, children_id: list[str]) -> None:
        for id in children_id:
            self._delete(self._block_endpoint(self.id))
            self.logger.info(f"Deleted child block `{id}`.")

    def restore_child(self, children_id: list[str]) -> None:
        for id in children_id:
            self._patch(self._block_endpoint(self.id), payload=b'{"archived": false}')
            self.logger.info(f"Restored child block `{id}`.")

    def update(
        self,
        payload: Union[
            MutableMapping[str, Any], Union[Iterable[bytes], bytes, bytearray]
        ],
    ) -> MutableMapping[str, Any]:
        """
        Updates content for the specified block_id based on the block
        type. Supported fields based on the block object type.
        Note: The update replaces the entire value for a given field.
        If a field is omitted (ex: omitting checked when updating a to_do block),
        the value will not be changed.

        To update title of a child_page block, use the pages endpoint
        To update title of a child_database block, use the databases endpoint

        Toggle can be added and removed from a heading block. However,
        you cannot remove toggle from a heading block if it has children
        All children MUST be removed before revoking toggle from a heading block

        https://developers.notion.com/reference/update-a-block
        """
        return self._patch(self._block_endpoint(self.id), payload=payload)
