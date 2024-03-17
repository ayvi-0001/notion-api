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

from typing import Any, Collection, MutableMapping, Optional, Sequence

from notion.properties.build import NotionObject
from notion.properties.common import _NotionURL
from notion.properties.files import ExternalFile
from notion.properties.options import BlockColor, CodeBlockLang
from notion.properties.richtext import Mention, RichText

__all__: Sequence[str] = (
    "BlockChildren",
    "OriginalSyncedBlockType",
    "DuplicateSyncedBlockType",
    "ParagraphBlocktype",
    "NewLineBreak",
    "CalloutBlocktype",
    "QuoteBlocktype",
    "BulletedListItemBlocktype",
    "NumberedListItemBlocktype",
    "ToDoBlocktype",
    "ToggleBlocktype",
    "CodeBlocktype",
    "EmbedBlocktype",
    "BookmarkBlocktype",
    "EquationBlocktype",
    "TableOfContentsBlocktype",
    "DividerBlock",
    "BreadcrumbBlock",
    "Heading1BlockType",
    "Heading2BlockType",
    "Heading3BlockType",
    "LinkToPageBlockType",
    "VideoBlockType",
    "ImageBlockType",
    "ColumnListBlockType",
    "TableBlockType",
    "TableRowBlockType",
)


class BlockChildren(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        block_type_objects_array: Optional[
            Sequence[NotionObject | MutableMapping[str, Any]]
        ] = None,
        after: Optional[str] = None,
    ) -> None:
        """https://developers.notion.com/reference/block"""
        super().__init__()
        if not block_type_objects_array:
            block_type_objects_array = []

        self.set("children", block_type_objects_array)

        if after:
            self.set("after", after)


class OriginalSyncedBlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, children: Optional[list[str]]) -> None:
        """https://developers.notion.com/reference/block#original-synced-block"""
        super().__init__()
        if not children:
            children = []

        self.set("type", "synced_block")
        self.nest("synced_block", "synced_from", None)
        self.nest("synced_block", "children", children)


class DuplicateSyncedBlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, block_id: str) -> None:
        """https://developers.notion.com/reference/block#duplicate-synced-block"""
        super().__init__()
        self.set("type", "synced_block")
        self.nest("synced_block", "synced_from", {"type": "block_id"})
        self.nest("synced_block", "synced_from", {"block_id": block_id})


class ParagraphBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[RichText | Mention],
        /,
        *,
        block_color: Optional[BlockColor | str] = None,
    ) -> None:
        """https://developers.notion.com/reference/block#paragraph"""
        super().__init__()
        if not block_color:
            block_color = BlockColor.default.value

        self.set("type", "paragraph")
        self.nest("paragraph", "rich_text", rich_text)
        self.nest("paragraph", "color", block_color)


NewLineBreak = ParagraphBlocktype([RichText("")])


class CalloutBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[RichText | Mention],
        /,
        *,
        icon: Optional[str] = None,
        block_color: Optional[BlockColor | str] = None,
    ) -> None:
        """https://developers.notion.com/reference/block#callout"""
        super().__init__()
        if not block_color:
            block_color = BlockColor.default.value

        self.set("type", "callout")
        self.nest("callout", "rich_text", rich_text)
        self.nest("callout", "color", block_color)
        if icon:
            self.nest("callout", "icon", ExternalFile(icon))


class QuoteBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[RichText | Mention],
        /,
        *,
        block_color: Optional[BlockColor | str] = None,
    ) -> None:
        """https://developers.notion.com/reference/block#quote"""
        super().__init__()
        if not block_color:
            block_color = BlockColor.default.value

        self.set("type", "quote")
        self.nest("quote", "rich_text", rich_text)
        self.nest("quote", "color", block_color)


class BulletedListItemBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[RichText | Mention],
        /,
        *,
        block_color: Optional[BlockColor | str] = None,
    ) -> None:
        """https://developers.notion.com/reference/block#bulleted-list-item"""
        super().__init__()
        if not block_color:
            block_color = BlockColor.default.value

        self.set("type", "bulleted_list_item")
        self.nest("bulleted_list_item", "rich_text", rich_text)
        self.nest("bulleted_list_item", "color", block_color)


class NumberedListItemBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[RichText | Mention],
        /,
        *,
        block_color: Optional[BlockColor | str] = None,
    ) -> None:
        """https://developers.notion.com/reference/block#numbered-list-item"""
        super().__init__()
        if not block_color:
            block_color = BlockColor.default.value

        self.set("type", "numbered_list_item")
        self.nest("numbered_list_item", "rich_text", rich_text)
        self.nest("numbered_list_item", "color", block_color)


class ToDoBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[RichText | Mention],
        /,
        *,
        checked: Optional[bool] = False,
        block_color: Optional[BlockColor | str] = None,
    ) -> None:
        """https://developers.notion.com/reference/block#to-do"""
        super().__init__()
        if not block_color:
            block_color = BlockColor.default.value

        self.set("type", "to_do")
        self.nest("to_do", "rich_text", rich_text)
        self.nest("to_do", "color", block_color)
        self.nest("to_do", "checked", checked)


class ToggleBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[RichText | Mention],
        /,
        *,
        block_color: Optional[BlockColor | str] = None,
    ) -> None:
        """https://developers.notion.com/reference/block#toggle-blocks"""
        super().__init__()
        if not block_color:
            block_color = BlockColor.default.value

        self.set("type", "toggle")
        self.nest("toggle", "rich_text", rich_text)
        self.nest("toggle", "color", block_color)


class CodeBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Optional[Sequence[RichText | Mention]] = None,
        /,
        *,
        language: Optional[CodeBlockLang | str] = None,
        caption: Optional[Sequence[RichText | Mention | str]] = None,
    ) -> None:
        """https://developers.notion.com/reference/block#code"""
        super().__init__()
        if not language:
            language = CodeBlockLang.plain_text.value

        if not rich_text:
            rich_text = [RichText("")]

        self.set("type", "code")
        self.nest("code", "rich_text", rich_text)
        self.nest("code", "language", language)
        self.nest("code", "caption", caption) if caption else None


class EmbedBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, embedded_url: str, /) -> None:
        """https://developers.notion.com/reference/block#embed"""
        super().__init__()
        self.set("type", "embed")
        self.set("embed", _NotionURL(embedded_url))


class BookmarkBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        bookmark_url: str,
        /,
        *,
        caption: Optional[Sequence[RichText | Mention]] = None,
    ) -> None:
        """https://developers.notion.com/reference/block#bookmark"""
        super().__init__()
        self.set("type", "bookmark")
        self.set("bookmark", _NotionURL(bookmark_url))
        self.nest("bookmark", "caption", caption) if caption else None


class EquationBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, expression: str) -> None:
        """https://developers.notion.com/reference/block#equation"""
        super().__init__()
        self.set("type", "equation")
        self.nest("equation", "expression", expression)


class TableOfContentsBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, block_color: Optional[BlockColor | str] = None) -> None:
        """https://developers.notion.com/reference/block#table-of-contents"""
        super().__init__()
        if not block_color:
            block_color = BlockColor.default.value

        self.set("type", "table_of_contents")
        self.nest("table_of_contents", "color", block_color)


class Heading1BlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[RichText | Mention],
        /,
        *,
        block_color: Optional[BlockColor | str] = None,
        is_toggleable: Optional[bool] = False,
    ) -> None:
        """https://developers.notion.com/reference/block#headings"""
        super().__init__()
        if not block_color:
            block_color = BlockColor.default.value

        self.set("type", "heading_1")
        self.nest("heading_1", "rich_text", rich_text)
        self.nest("heading_1", "color", block_color)
        self.nest("heading_1", "is_toggleable", is_toggleable)


class Heading2BlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[RichText | Mention],
        /,
        *,
        block_color: Optional[BlockColor | str] = None,
        is_toggleable: Optional[bool] = False,
    ) -> None:
        """https://developers.notion.com/reference/block#headings"""
        super().__init__()
        if not block_color:
            block_color = BlockColor.default.value

        self.set("type", "heading_2")
        self.nest("heading_2", "rich_text", rich_text)
        self.nest("heading_2", "color", block_color)
        self.nest("heading_2", "is_toggleable", is_toggleable)


class Heading3BlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[RichText | Mention],
        /,
        *,
        block_color: Optional[BlockColor | str] = None,
        is_toggleable: Optional[bool] = False,
    ) -> None:
        """https://developers.notion.com/reference/block#headings"""
        super().__init__()
        if not block_color:
            block_color = BlockColor.default.value

        self.set("type", "heading_3")
        self.nest("heading_3", "rich_text", rich_text)
        self.nest("heading_3", "color", block_color)
        self.nest("heading_3", "is_toggleable", is_toggleable)


class LinkToPageBlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, page_id: str) -> None:
        """https://developers.notion.com/reference/block#link-to-page"""
        super().__init__()
        self.set("type", "link_to_page")
        self.nest("link_to_page", "type", "page_id")
        self.nest("link_to_page", "page_id", page_id)


class BreadcrumbBlock(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self) -> None:
        """https://developers.notion.com/reference/block#breadcrumb"""
        super().__init__()
        self.set("type", "breadcrumb")
        self.set("breadcrumb", {})


class DividerBlock(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self) -> None:
        """https://developers.notion.com/reference/block#divider"""
        super().__init__()
        self.set("type", "divider")
        self.set("divider", {})


class VideoBlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, url: str) -> None:
        """https://developers.notion.com/reference/block#video"""
        super().__init__()
        self.set("type", "video")
        self.set("video", ExternalFile(url))


class ImageBlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, url: str) -> None:
        """https://developers.notion.com/reference/block#image"""
        super().__init__()
        self.set("type", "image")
        self.set("image", ExternalFile(url))


class TableBlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        table_width: int | None = None,
        has_column_header: bool | None = None,
        has_row_header: bool | None = None,
        children: Sequence[NotionObject | MutableMapping[str, Any]] | None = None,
    ) -> None:
        """https://developers.notion.com/reference/block#table"""
        super().__init__()
        self.set("type", "table")
        self.nest("table", "table_width", table_width)
        self.nest("table", "has_column_header", has_column_header)
        self.nest("table", "has_row_header", has_row_header)
        self.nest("table", "children", children)


class TableRowBlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self, cells: Sequence[list[dict[str, Collection[str]]]] | None = None
    ) -> None:
        """https://developers.notion.com/reference/block#table-rows"""
        super().__init__()
        self.set("type", "table_row")
        self.nest("table_row", "cells", cells)
