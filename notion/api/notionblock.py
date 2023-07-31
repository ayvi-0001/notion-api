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
"""
A block object represents a piece of content within Notion. 
The API translates the headings, toggles, paragraphs, lists, media, and more that you can interact with in the Notion UI as different block type objects.
Block types which support children are:
    "paragraph", "bulleted_list_item", "numbered_list_item", "toggle", "to_do", "quote", "callout",
    "synced_block", "column", "child_page", "child_database", and "table".
    
    All heading blocks ("heading_1", "heading_2", and "heading_3") support children when the is_toggleable property is true.

NOTE: The link_preview block will only be returned as part of a response. It cannot be created via the API.
NOTE: As of March 27, 2023, Notion is no longer supporting the creation of template blocks. They are not included in this module.

https://developers.notion.com/reference/block
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any, MutableMapping, Optional, Sequence, cast

from notion.api.block_ext import (
    CELLS_ARRAY,
    CodeBlock,
    EquationBlock,
    TableBlock,
    ToDoBlock,
)
from notion.api.blockmixin import _TokenBlockMixin
from notion.api.client import _NLOG
from notion.properties.blocktypes import (
    BlockChildren,
    BookmarkBlocktype,
    BreadcrumbBlock,
    BulletedListItemBlocktype,
    CalloutBlocktype,
    CodeBlocktype,
    DividerBlock,
    DuplicateSyncedBlockType,
    EmbedBlocktype,
    EquationBlocktype,
    Heading1BlockType,
    Heading2BlockType,
    Heading3BlockType,
    ImageBlockType,
    LinkToPageBlockType,
    NewLineBreak,
    NumberedListItemBlocktype,
    OriginalSyncedBlockType,
    ParagraphBlocktype,
    QuoteBlocktype,
    TableBlockType,
    TableOfContentsBlocktype,
    TableRowBlockType,
    ToDoBlocktype,
    ToggleBlocktype,
    VideoBlockType,
)
from notion.properties.options import BlockColor, CodeBlockLang
from notion.properties.richtext import Mention, RichText

if TYPE_CHECKING:
    from notion.api.notionpage import Page


__all__: Sequence[str] = ["Block"]


class Block(_TokenBlockMixin):
    """A block object represents content within Notion.
    Blocks can be text, lists, media, and more. A page is a type of block, too.

    These are the individual 'nodes' in a page that you typically interact with in Notion.
    Some blocks have more content nested inside them.
    Some examples are indented paragraphs, lists, and toggles.
    The nested content is called children, and children are blocks, too.

    ---
    ### Versioning:
    To use a previous version of the API, set the envrionment variable `NOTION_VERSION`.
    For more info see: https://developers.notion.com/reference/versioning

    ---
    :param id:    (required) `block_id` of object in Notion.
    :param token: (optional) Bearer token provided when you create an integration.\
                  Set notion secret in environment variables as `NOTION_TOKEN`, or set variable here.\
                  See https://developers.notion.com/reference/authentication.

    https://developers.notion.com/reference/block
    """

    def __init__(self, id: str, /, *, token: Optional[str] = None) -> None:
        super().__init__(id, token=token)
        self.logger = _NLOG.getChild(self.__repr__())

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
        self, payload: MutableMapping[str, Any] | str | bytes | bytearray
    ) -> MutableMapping[str, Any]:
        """
        Creates/appends new children blocks to the parent block_id specified.
        Returns a paginated list of newly created children block objects.

        https://developers.notion.com/reference/patch-block-children
        """
        return self._patch(self._block_endpoint(self.id, children=True), payload=payload)

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
        if self.is_archived:
            return None

        self._delete(self._block_endpoint(self.id))

    @property
    def restore_self(self) -> None:
        """
        Sets "archived" key to false. Parent page must still exist in Notion's trash.
        :returns: If block is archived, a Mapping of the restored block object, else None.

        https://developers.notion.com/reference/update-a-block
        """
        if not self.is_archived:
            return None

        self._patch(self._block_endpoint(self.id), payload=(b'{"archived": false}'))

    def delete_child(
        self, children_id: Optional[list[str]] = None, *, all: Optional[bool] = False
    ) -> None:
        if not self.has_children:
            return

        if all:
            children = [block["id"] for block in self.retrieve_children()["results"]]
            for id in children:
                self._delete(self._block_endpoint(id))
            return

        if children_id:
            for id in children_id:
                self._delete(self._block_endpoint(id))

    def update(
        self, payload: MutableMapping[str, Any] | str | bytes | bytearray
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

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BLOCK FACTORY METHODS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    # Factory methods used to create and append new children blocks to the parent block_id specified.
    # Blocks can be parented by other blocks, pages, or databases
    # All methods require a parent instance of either notion.Block or notion.Page
    # By default, blocks are appended to the bottom of the parent block.
    # To append a block in a specific place other than the bottom of the parent block,
    # use the "after" parameter and set its value to the ID of the block that the new block should be appended after.
    # Once a block is appended as a child, it can't be moved elsewhere via the API.

    # Most methods return a `Block` object, which can be used to continously nest blocks.
    # For blocks that allow children, Notion allows up to two levels of nesting in a single request.
    # Each method of `Block` is a separate request to the API and is not affected by this limitation.

    # Some methods return a specialized `Block` object, these include:
    # Codeblock, EquationBlock, TodoBlock, TableBlock, and RichTextBlock.
    # RichTextBlock refers to any block that contains text that can be formatted.
    # These are:  "paragraph", "to_do", "toggle", "quote", "callout"
    #             "bulleted_list_item", "numbered_list_item",
    #             "headings", "toggle_headings"
    # See examples in repo for specific functions for blocks above.

    # Example
    # ```py
    # notion.Block.divider(
    #     notion.Block.paragraph(
    #         notion.Block.paragraph(
    #             notion.Block('87aadab8ce4b407682197c922e51511f'
    #             ), ['This is the parent']
    #         ), ['This is the child']
    #     )
    # )
    # ```
    # will output in Notion:
    # ```md
    # This is block 87aadab8ce4b407682197c922e51511f
    #     This is the parent
    #         This is the child
    #             ---
    # ```

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SYNCED BLOCK TYPES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    @classmethod
    def original_synced_block(
        cls, parent_object: Page | Block, after: Optional[str] = None
    ) -> Block:
        """Creates an empty synced block that can be appended to other blocks with `notion.Block.duplicate_synced_block(...)`.

        ### Original Synced Block
        Similar to the UI, there are two versions of a synced_block --
        the original block that was created first and doesn't yet sync with anything else,
        and the reference blocks that are synced to the original synced block.

        To create a synced_block, the developer needs to create an original synced block.
        Developers will be able to identify the original synced_block because it does not
        "sync_from" any other block (synced_from property is set to null).

        Note that all of the blocks available to be synced in another synced_block must be captured in the children property.

        `synced_from` Value is always null to signify that this is an original synced block and that is not referring to another block

        https://developers.notion.com/reference/block#original-synced-block

        :returns: A new `notion.api.Block` object with the `block_id` of the original synced block.
        """
        block_mapping = parent_object._append(
            BlockChildren([OriginalSyncedBlockType(children=[])], after=after)
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def duplicate_synced_block(
        cls, parent_object: Page | Block, block_id: str, after: Optional[str] = None
    ) -> Block:
        """### Reference Synced Block
        To sync the content of the original synced_block with another synced_block,
        the developer simply needs to refer to that synced_block using the synced_from property.

        Note that only "original" synced blocks can be referenced in the synced_from property.

        https://developers.notion.com/reference/block#duplicate-synced-block

        :param block_id: (required) string (UUIDv4). Identifier of an original synced_block
        :returns: A new `notion.api.Block` object with the `block_id` of the duplicate synced block.
        """
        block_mapping = parent_object._append(
            BlockChildren([DuplicateSyncedBlockType(block_id)], after=after)
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BLOCK EXTENSIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # ~~~~~~~~~~~ These return custom blocks with unique methods to their block type ~~~~~~~~~~~ #

    @staticmethod
    def code(
        parent_object: Page | Block,
        code_text: Optional[str] = None,
        *,
        language: Optional[CodeBlockLang | str] = None,
        caption: Optional[Sequence[RichText | Mention | str]] = None,
        after: Optional[str] = None,
    ) -> CodeBlock:
        """Creates a code block. https://developers.notion.com/reference/block#code-blocks

        :returns: `notion.api.block_ext.CodeBlock` object.
        :raises: NotionValidationError if code block is >= 2000 characters.
        """
        block_mapping = parent_object._append(
            BlockChildren(
                [
                    CodeBlocktype(
                        [RichText(code_text)], language=language, caption=caption
                    )
                ],
                after=after,
            )
        )
        return CodeBlock(cast(str, block_mapping["results"][0]["id"]))

    @staticmethod
    def table(
        parent_object: Page | Block,
        *,
        table_width: int = 2,
        has_column_header: bool = False,
        has_row_header: bool = False,
        after: Optional[str] = None,
    ) -> TableBlock:
        """
        Note that the number of columns in a table can only be set when the table is first created.
        Calls to the Update block endpoint to update table_width fail.
        See examples in repo for more details.

        Table:      https://developers.notion.com/reference/block#table
        Table Rows: https://developers.notion.com/reference/block#table-rows

        :returns: `notion.api.block_ext.TableBlock` object.

        :param table_width: The number of columns in the table.\
                            Note that this cannot be changed via the public API once a table is created.
        :param has_column_header: Whether the table has a column header.\
                                  If true, then the first row in the table appears visually distinct from the other rows.
        :param has_row_header: Whether the table has a row header.\
                                  If true, then the first column in the table appears visually distinct from the other columns.
        """
        cells: CELLS_ARRAY = [[] for _ in range(table_width)]
        rows = [TableRowBlockType(cells)]
        block_mapping = parent_object._append(
            BlockChildren(
                [
                    TableBlockType(
                        table_width, has_column_header, has_row_header, children=rows
                    )
                ],
                after=after,
            )
        )
        return TableBlock(cast(str, block_mapping["results"][0]["id"]))

    @staticmethod
    def to_do(
        parent_object: Page | Block,
        rich_text: Sequence[RichText | Mention],
        *,
        block_color: Optional[BlockColor | str] = None,
        checked: Optional[bool] = False,
        after: Optional[str] = None,
    ) -> ToDoBlock:
        """Creates a to-do block. https://developers.notion.com/reference/block#to-do-blocks

        :returns: `notion.api.block.ToDoBlock` object.
        """
        block_mapping = parent_object._append(
            BlockChildren(
                [ToDoBlocktype(rich_text, block_color=block_color, checked=checked)],
                after=after,
            )
        )
        return ToDoBlock(cast(str, block_mapping["results"][0]["id"]))

    @staticmethod
    def equation(
        parent_object: Page | Block, expression: str, /, *, after: Optional[str] = None
    ) -> EquationBlock:
        """Creates an equation block. https://developers.notion.com/reference/block#equation-blocks

        :param expression: (required) A KaTeX compatible string.
        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren([EquationBlocktype(expression)], after=after)
        )
        return EquationBlock(cast(str, block_mapping["results"][0]["id"]))

    # ~~~~~~~~~~~~~~ TEXT-EDITABLE BLOCKS (Can be used by `notion.RichTextBlock`) ~~~~~~~~~~~~~~ #

    @classmethod
    def paragraph(
        cls,
        parent_object: Page | Block,
        rich_text: Sequence[RichText | Mention],
        *,
        after: Optional[str] = None,
        block_color: Optional[BlockColor | str] = None,
    ) -> Block:
        """Creates a paragraph block. https://developers.notion.com/reference/block#paragraph-blocks

        :param rich_text: list of `notion.properties.RichText` objects.
        :param after: The ID of the existing block that the new block should be appended after.

        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren(
                [ParagraphBlocktype(rich_text, block_color=block_color)], after=after
            )
        )

        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def quote(
        cls,
        parent_object: Page | Block,
        rich_text: Sequence[RichText | Mention],
        *,
        after: Optional[str] = None,
        block_color: Optional[BlockColor | str] = None,
    ) -> Block:
        """Creates a quote block. https://developers.notion.com/reference/block#quote-blocks

        :param rich_text: list of `notion.properties.RichText` objects.
        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren(
                [QuoteBlocktype(rich_text, block_color=block_color)], after=after
            )
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def callout(
        cls,
        parent_object: Page | Block,
        rich_text: Sequence[RichText | Mention],
        *,
        icon: Optional[str] = None,
        after: Optional[str] = None,
        block_color: Optional[BlockColor | str] = None,
    ) -> Block:
        """Creates a callout block. https://developers.notion.com/reference/block#callout-blocks

        :param rich_text: list of `notion.properties.RichText` objects.
        :param icon: url to external source for icon.
        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren(
                [CalloutBlocktype(rich_text, icon=icon, block_color=block_color)],
                after=after,
            )
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def heading1(
        cls,
        parent_object: Page | Block,
        rich_text: Sequence[RichText | Mention],
        *,
        is_toggleable: Optional[bool] = False,
        after: Optional[str] = None,
        block_color: Optional[BlockColor | str] = None,
    ) -> Block:
        """Creates a heading 1 block. https://developers.notion.com/reference/block#heading-one-blocks

        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren(
                [
                    Heading1BlockType(
                        rich_text, block_color=block_color, is_toggleable=is_toggleable
                    )
                ],
                after=after,
            )
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def heading2(
        cls,
        parent_object: Page | Block,
        rich_text: Sequence[RichText | Mention],
        *,
        is_toggleable: Optional[bool] = False,
        after: Optional[str] = None,
        block_color: Optional[BlockColor | str] = None,
    ) -> Block:
        """Creates a heading 2 block. https://developers.notion.com/reference/block#heading-two-blocks

        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren(
                [
                    Heading2BlockType(
                        rich_text, block_color=block_color, is_toggleable=is_toggleable
                    )
                ],
                after=after,
            )
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def heading3(
        cls,
        parent_object: Page | Block,
        rich_text: Sequence[RichText | Mention],
        *,
        is_toggleable: Optional[bool] = False,
        after: Optional[str] = None,
        block_color: Optional[BlockColor | str] = None,
    ) -> Block:
        """Creates a heading 3 block. https://developers.notion.com/reference/block#heading-three-blocks

        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren(
                [
                    Heading3BlockType(
                        rich_text, block_color=block_color, is_toggleable=is_toggleable
                    )
                ],
                after=after,
            )
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def bulleted_list(
        cls,
        parent_object: Page | Block,
        rich_text: Sequence[RichText | Mention],
        *,
        after: Optional[str] = None,
        block_color: Optional[BlockColor | str] = None,
    ) -> Block:
        """Creates a bulleted list block. https://developers.notion.com/reference/block#bulleted-list-item-blocks

        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren(
                [BulletedListItemBlocktype(rich_text, block_color=block_color)],
                after=after,
            )
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def numbered_list(
        cls,
        parent_object: Page | Block,
        rich_text: Sequence[RichText | Mention],
        *,
        after: Optional[str] = None,
        block_color: Optional[BlockColor | str] = None,
    ) -> Block:
        """Creates a numbered list block. https://developers.notion.com/reference/block#numbered-list-item-blocks

        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren(
                [NumberedListItemBlocktype(rich_text, block_color=block_color)],
                after=after,
            )
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def toggle(
        cls,
        parent_object: Page | Block,
        rich_text: Sequence[RichText | Mention],
        *,
        after: Optional[str] = None,
        block_color: Optional[BlockColor | str] = None,
    ) -> Block:
        """Creates a toggle block. https://developers.notion.com/reference/block#toggle-blocks

        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren(
                [ToggleBlocktype(rich_text, block_color=block_color)], after=after
            )
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ EXTERNAL URL BLOCKS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    @classmethod
    def embed_url(
        cls,
        parent_object: Page | Block,
        embedded_url: str,
        /,
        after: Optional[str] = None,
    ) -> Block:
        """
        ##### WARNING: embed block types through the API are not reliable and often cause errors.

        Embed block types are:
        Framer, Twitter (tweets), Google Drive documents, Gist, Figma,
        Invision, Loom, Typeform, Codepen, PDFs, Google Maps, Whimisical,
        Miro, Abstract, excalidraw, Sketch, Replit
        There is no need to specify the specific embed type, only the URL.

        ### Differences in embed blocks between the Notion app and the API
        The Notion app uses a 3rd-party service, Embedly, to validate and request metadata for embeds given a URL.
        This works well in a web app because Notion can kick off an asynchronous request for URL information,
        which might take seconds or longer to complete, and then update the block with the metadata in the UI
        after receiving a response from Embedly.

        Embedly is not called when creating embed blocks in the API because the API needs to be able to return
        faster than the UI, and because the response from Embedly could actually cause us change the block type.
        This would result in a slow and potentially confusing experience as the block in the response would
        not match the block sent in the request.
        The result is that embed blocks created via the API may not look exactly
        like their counterparts created in the Notion app.

        https://developers.notion.com/reference/block#embed-blocks

        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren([EmbedBlocktype(embedded_url)], after=after)
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def video(
        cls, parent_object: Page | Block, url: str, /, after: Optional[str] = None
    ) -> Block:
        """Creates a video block. https://developers.notion.com/reference/block#video
        Supported video types:
        .amv .asf .avi .f4v .flv .gifv .mkv .mov .mpg .mpeg .mpv .mp4 .m4v .qt .wmv

        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren([VideoBlockType(url)], after=after)
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def image(
        cls, parent_object: Page | Block, url: str, /, after: Optional[str] = None
    ) -> Block:
        """Creates an image block.
        Supported image types: .bmp .gif .heic .jpeg .jpg .png .svg .tif .tiff
        https://developers.notion.com/reference/block#image
        """
        block_mapping = parent_object._append(
            BlockChildren([ImageBlockType(url)], after=after)
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def bookmark(
        cls,
        parent_object: Page | Block,
        bookmark_url: str,
        *,
        after: Optional[str] = None,
        caption: Optional[Sequence[RichText | Mention]] = None,
    ) -> Block:
        """Creates a bookmark block. https://developers.notion.com/reference/block#bookmark-blocks

        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren([BookmarkBlocktype(bookmark_url, caption=caption)], after=after)
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MISC BLOCKS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    @classmethod
    def link_to_page(
        cls, parent_object: Page | Block, page_id: str, /, after: Optional[str] = None
    ) -> Block:
        """Creates a link_to_page block. https://developers.notion.com/reference/block#link-to-page-blocks

        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren([LinkToPageBlockType(page_id)], after=after)
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def table_of_contents(
        cls,
        parent_object: Page | Block,
        *,
        after: Optional[str] = None,
        block_color: Optional[BlockColor | str] = None,
    ) -> Block:
        """Creates a table of contents block.
        https://developers.notion.com/reference/block#table-of-contents-blocks

        :returns: `notion.api.Block`
        """
        block_mapping = parent_object._append(
            BlockChildren(
                [TableOfContentsBlocktype(block_color=block_color)], after=after
            )
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def breadcrumb(
        cls, parent_object: Page | Block, after: Optional[str] = None
    ) -> Block:
        """Creates a breadcrumb block.
        https://developers.notion.com/reference/block#breadcrumb-blocks
        """
        block_mapping = parent_object._append(
            BlockChildren([BreadcrumbBlock()], after=after)
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def divider(cls, parent_object: Page | Block, after: Optional[str] = None) -> Block:
        """Creates a divider block.
        https://developers.notion.com/reference/block#divider-blocks
        """
        block_mapping = parent_object._append(
            BlockChildren([DividerBlock()], after=after)
        )
        return cls(cast(str, block_mapping["results"][0]["id"]))

    @classmethod
    def newline(cls, parent_object: Page | Block, after: Optional[str] = None) -> Block:
        """Creates a newline break."""
        block_mapping = parent_object._append(BlockChildren([NewLineBreak], after=after))
        return cls(cast(str, block_mapping["results"][0]["id"]))

    # Column blocks are not currently supported by this library.
