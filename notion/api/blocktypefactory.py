# MIT License

# Copyright (c) 2023 ayvi#0001

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
A block object represents content within Notion. Blocks can be text, lists, media, and more. A page is a type of block, too.
Some blocks have more content nested inside them. Some examples are indented paragraphs, lists, and toggles. 
The nested content is called children, and children are blocks, too.

Block types that support children
Block types which support children are:
    "paragraph", "bulleted_list_item", "numbered_list_item", "toggle", "to_do", "quote", "callout", 
    "synced_block", "template", "column", "child_page", "child_database", and "table". 
    All heading blocks ("heading_1", "heading_2", and "heading_3") support children when the is_toggleable property is true.

NOTE: The link_preview block will only be returned as part of a response. It cannot be created via the API.

https://developers.notion.com/reference/block
"""
from __future__ import annotations
from typing import Sequence
from typing import Union
from typing import Optional
from typing import cast
from functools import reduce
from operator import getitem
from operator import methodcaller
from functools import singledispatchmethod

from notion.properties import *
from notion.core.typedefs import *
from notion.api.notionpage import Page
from notion.api.notionblock import Block
from notion.api.client import _NotionClient
from notion.properties.richtext import RichTextTypeObject

__all__: Sequence[str] = ["BlockFactory"]


class BlockFactory(_NotionClient):
    """
    Factory to write block types as a child of the target
    `notion.api.notionblock.Block` or `notion.api.notionpage.Page`.
    Returns an instance of `notion.api.notionblock.Block`.

    To recurisvely set children blocks, each method will return the new block object,
    which contains the `block_id` that can be extracted for the `target`
    OR
    nest `Blockfactory` with the outermost method being the last nested block.
    ```py
    notion.BlockFactory.divider(
        notion.BlockFactory.paragraph(
            notion.BlockFactory.paragraph(
                notion.Block('87aadab8ce4b407682197c922e51511f'
                ), ['This is the parent']
            ), ['This is the child']
        )
    )
    ```
    will output in Notion:
    ```md
    This is block 87aadab8ce4b407682197c922e51511f
        This is the parent
            This is the child
                ---
    ```
    NOTE: Nested Children
    For blocks that allow children, we allow up to two levels of nesting in a single request.
    """

    def __init__(self) -> None:
        pass

    @singledispatchmethod
    @staticmethod
    def _append(target, payload) -> Block:
        ...

    @_append.register
    @staticmethod
    def _(target: Union[Page, Block], payload: JSONObject) -> Block:
        _append_method = methodcaller("_append", payload=payload)
        new_block = _append_method(target)
        id_new_block = str(reduce(getitem, ["results", 0, "id"], new_block))
        return Block(id_new_block)

    @_append.register
    @staticmethod
    def _(target: dict, payload: JSONObject) -> Block:
        """
        If target is not an instance of Page or Block,
        It can also be a block object from a list of results
        ```json
        {
            "object": "list",
            "results": [
                {
                    "object": "block",
                    "id": "9dd8e0d6-8370-4f19-914b-39abc9863c1a",
                    // ...
                }
            ],
            "next_cursor": null,
            "has_more": false,
            "type": "block",
            "block": {}
        }
        ```
        or a block object directly
        ```json
        {
            "object": "block",
            "id": "647eec30-e714-4c5f-908f-73ab2f6e8c99"
            // ...
        }
        ```
        """
        if target["object"] == "list":
            assert "type" in target and target["block"] == {}
            id_target = str(reduce(getitem, ["results", 0, "id"], target))
            new_block = cast("dict", Block(id_target)._append(payload))
            id_new_block = str(reduce(getitem, ["results", 0, "id"], new_block))

            return Block(id_new_block)
        else:
            assert target["object"] == "block"
            new_block = cast("dict", Block(target["id"])._append(payload))
            id_new_block = str(reduce(getitem, ["results", 0, "id"], new_block))

            return Block(id_new_block)

    @staticmethod
    def reference_synced_block(
        target: Union[Page, Block, JSONObject], block_id: str
    ) -> Block:
        """
        ### Reference Synced Block
        To sync the content of the original synced_block with another synced_block,
        the developer simply needs to refer to that synced_block using the synced_from property.

        Note that only "original" synced blocks can be referenced in the synced_from property.

        ---
        :param block_id: (required) string (UUIDv4). Identifier of an original synced_block

        https://developers.notion.com/reference/block#synced-block-blocks
        """

        return BlockFactory._append(
            target, Children([ReferenceSyncedBlockType(block_id)])
        )

    @staticmethod
    def new_synced_block(target: Union[Page, Block, JSONObject]) -> Block:
        """
        Similar to the UI, there are two versions of a synced_block --
        the original block that was created first and doesn't yet sync with anything else,
        and the reference blocks that are synced to the original synced block.

        ### Original Synced Block
        To create a synced_block, the developer needs to create an original synced block.
        Developers will be able to identify the original synced_block because it does not
        "sync_from" any other block (synced_from property is set to null).

        Note that all of the blocks available to be synced in another synced_block must be captured in the children property.

        `synced_from` Value is always null to signify that this is an original synced block and that is not referring to another block

        ---
        This method will create a new _empty_ synced block that can be
        appended to other blocks with `BlockWrite.reference_synced_block(...)`.
        return it to get the new block id and use as a target to append new children.

        View `notion.properties.blocktypes.OriginalSyncedBlock`, or Notion API reference
        for more information.

        https://developers.notion.com/reference/block#synced-block-blocks
        """

        payload = Children([OriginalSyncedBlockType(children=[])])
        return BlockFactory._append(target, payload)

    @staticmethod
    def breadcrumb(target: Union[Page, Block, JSONObject]) -> Block:
        """https://developers.notion.com/reference/block#breadcrumb-blocks"""
        return BlockFactory._append(target, Children([BreadcrumbBlock]))

    @staticmethod
    def divider(target: Union[Page, Block, JSONObject]) -> Block:
        """https://developers.notion.com/reference/block#divider-blocks"""
        return BlockFactory._append(target, Children([DividerBlock]))

    @staticmethod
    def newline(target: Union[Page, Block, JSONObject]) -> Block:
        return BlockFactory._append(target, Children([NewLineBreak]))

    @staticmethod
    def quote(
        target: Union[Page, Block, JSONObject],
        rich_text: list[RichTextTypeObject],
        /,
        *,
        block_color: Optional[Union[NotionColors, str]] = None,
    ) -> Block:
        """https://developers.notion.com/reference/block#quote-blocks"""
        return BlockFactory._append(
            target, Children([QuoteBlocktype(rich_text, block_color=block_color)])
        )

    @staticmethod
    def callout(
        target: Union[Page, Block, JSONObject],
        rich_text: list[RichTextTypeObject],
        /,
        *,
        icon: Optional[str] = None,
        block_color: Optional[Union[NotionColors, str]] = None,
    ) -> Block:
        """
        :param icon: url to external source for icon.

        ---
        https://developers.notion.com/reference/block#callout-blocks
        """
        return BlockFactory._append(
            target,
            Children([CalloutBlocktype(rich_text, icon=icon, block_color=block_color)]),
        )

    @staticmethod
    def paragraph(
        target: Union[Page, Block, JSONObject],
        rich_text: list[RichTextTypeObject],
        /,
        *,
        block_color: Optional[Union[NotionColors, str]] = None,
    ) -> Block:
        """https://developers.notion.com/reference/block#paragraph-blocks"""
        return BlockFactory._append(
            target, Children([ParagraphBlocktype(rich_text, block_color=block_color)])
        )

    @staticmethod
    def heading1(
        target: Union[Page, Block, JSONObject],
        rich_text: list[RichTextTypeObject],
        /,
        *,
        block_color: Optional[Union[NotionColors, str]] = None,
        is_toggleable: Optional[bool] = False,
    ) -> Block:
        """https://developers.notion.com/reference/block#heading-one-blocks"""
        return BlockFactory._append(
            target,
            Children(
                [
                    Heading1BlockType(
                        rich_text, block_color=block_color, is_toggleable=is_toggleable
                    )
                ]
            ),
        )

    @staticmethod
    def heading2(
        target: Union[Page, Block, JSONObject],
        rich_text: list[RichTextTypeObject],
        /,
        *,
        block_color: Optional[Union[NotionColors, str]] = None,
        is_toggleable: Optional[bool] = False,
    ) -> Block:
        """https://developers.notion.com/reference/block#heading-two-blocks"""
        return BlockFactory._append(
            target,
            Children(
                [
                    Heading2BlockType(
                        rich_text, block_color=block_color, is_toggleable=is_toggleable
                    )
                ]
            ),
        )

    @staticmethod
    def heading3(
        target: Union[Page, Block, JSONObject],
        rich_text: list[RichTextTypeObject],
        /,
        *,
        block_color: Optional[Union[NotionColors, str]] = None,
        is_toggleable: Optional[bool] = False,
    ) -> Block:
        """https://developers.notion.com/reference/block#heading-three-blocks"""
        return BlockFactory._append(
            target,
            Children(
                [
                    Heading3BlockType(
                        rich_text, block_color=block_color, is_toggleable=is_toggleable
                    )
                ]
            ),
        )

    @staticmethod
    def bulleted_list(
        target: Union[Page, Block, JSONObject],
        rich_text: list[RichTextTypeObject],
        /,
        *,
        block_color: Optional[Union[NotionColors, str]] = None,
    ) -> Block:
        """https://developers.notion.com/reference/block#bulleted-list-item-blocks"""
        return BlockFactory._append(
            target,
            Children([BulletedListItemBlocktype(rich_text, block_color=block_color)]),
        )

    @staticmethod
    def numbered_list(
        target: Union[Page, Block, JSONObject],
        rich_text: list[RichTextTypeObject],
        /,
        *,
        block_color: Optional[Union[NotionColors, str]] = None,
    ) -> Block:
        """https://developers.notion.com/reference/block#numbered-list-item-blocks"""
        return BlockFactory._append(
            target,
            Children([NumberedListItemBlocktype(rich_text, block_color=block_color)]),
        )

    @staticmethod
    def to_do(
        target: Union[Page, Block, JSONObject],
        rich_text: list[RichTextTypeObject],
        /,
        *,
        block_color: Optional[Union[NotionColors, str]] = None,
        checked: Optional[bool] = False,
    ) -> Block:
        """https://developers.notion.com/reference/block#to-do-blocks"""
        return BlockFactory._append(
            target,
            Children(
                [ToDoBlocktype(rich_text, block_color=block_color, checked=checked)]
            ),
        )

    @staticmethod
    def toggle(
        target: Union[Page, Block, JSONObject],
        rich_text: list[RichTextTypeObject],
        /,
        *,
        block_color: Optional[Union[NotionColors, str]] = None,
    ) -> Block:
        """https://developers.notion.com/reference/block#toggle-blocks"""

        return BlockFactory._append(
            target, Children([ToggleBlocktype(rich_text, block_color=block_color)])
        )

    @staticmethod
    def code(
        target: Union[Page, Block, JSONObject],
        rich_text: list[RichTextTypeObject],
        /,
        *,
        language: NotionCodeLang | Optional[str] = None,
        caption: list[RichTextTypeObject] | None = None,
    ) -> Block:
        """
        raises:
        ```py
        notion.exceptions.errors.NotionValidationError: body failed validation:
        body.children[0].code.rich_text[0].text.content.length should be ≤ `2000`, instead was `57839`.

        https://developers.notion.com/reference/block#code-blocks
        """
        return BlockFactory._append(
            target,
            Children([CodeBlocktype(rich_text, language=language, caption=caption)]),
        )

    @staticmethod
    def embed_url(
        target: Union[Page, Block, JSONObject], embedded_url: str, /
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
        """
        return BlockFactory._append(target, Children([EmbedBlocktype(embedded_url)]))

    @staticmethod
    def bookmark(
        target: Union[Page, Block, JSONObject],
        bookmark_url: str,
        /,
        *,
        caption: list[RichTextTypeObject] | None = None,
    ) -> Block:
        """https://developers.notion.com/reference/block#bookmark-blocks"""

        return BlockFactory._append(
            target, Children([BookmarkBlocktype(bookmark_url, caption=caption)])
        )

    @staticmethod
    def link_to_page(target: Union[Page, Block, JSONObject], page_id: str, /) -> Block:
        """https://developers.notion.com/reference/block#link-to-page-blocks"""

        payload = Children([LinkToPageBlockType(page_id)])
        return BlockFactory._append(target, payload)

    @staticmethod
    def equation(target: Union[Page, Block, JSONObject], expression: str, /) -> Block:
        """
        :param expression: (required) A KaTeX compatible string

        ---
        https://developers.notion.com/reference/block#equation-blocks
        """
        return BlockFactory._append(target, Children([EquationBlocktype(expression)]))

    @staticmethod
    def table_of_contents(
        target: Union[Page, Block, JSONObject],
        /,
        *,
        block_color: Optional[Union[NotionColors, str]] = None,
    ) -> Block:
        """https://developers.notion.com/reference/block#table-of-contents-blocks"""
        return BlockFactory._append(
            target, Children([TableOfContentsBlocktype(block_color=block_color)])
        )


# TODO
# "FileBlocktype",
# "PdfBlocktype",
# ImageBlocktype,
# VideoBlocktype,
# "TemplateBlocktype",
# "ColumnBlocktype",
# "ColumnList",
# "TableBlocktype",
# "TableRowBlocktype"
