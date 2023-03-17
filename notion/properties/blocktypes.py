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

from typing import Optional, Sequence, Union

from notion.properties.build import NotionObject
from notion.properties.common import NotionURL
from notion.properties.files import ExternalFile
from notion.properties.options import BlockColor, CodeBlockLang
from notion.properties.richtext import Equation, Mention, RichText

# See docs in `notion.api.blockwrite.BlockFactory` for info on block types.

__all__: Sequence[str] = (
    "Children",
    "OriginalSyncedBlockType",
    "ReferenceSyncedBlockType",
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
)


class Children(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        block_type_objects_array: Optional[list[NotionObject]],
    ) -> None:
        super().__init__()
        if not block_type_objects_array:
            block_type_objects_array = []

        self.set("children", block_type_objects_array)


class OriginalSyncedBlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, children: Optional[list[str]]) -> None:
        super().__init__()
        if not children:
            children = []

        self.set("type", "synced_block")
        self.nest("synced_block", "synced_from", None)
        self.nest("synced_block", "children", children)


class ReferenceSyncedBlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, block_id: str) -> None:
        super().__init__()
        self.set("type", "synced_block")
        self.nest("synced_block", "synced_from", {"type": "block_id"})
        self.nest("synced_block", "synced_from", {"block_id": block_id})


class ParagraphBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[Union[RichText, Mention, Equation]],
        /,
        *,
        block_color: Optional[Union[BlockColor, str]] = None,
    ) -> None:
        super().__init__()

        if not block_color:
            block_color = BlockColor.default

        self.set("type", "paragraph")
        self.nest("paragraph", "rich_text", rich_text)
        self.nest("paragraph", "color", block_color)


NewLineBreak = ParagraphBlocktype([RichText("")])


class CalloutBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[Union[RichText, Mention, Equation]],
        /,
        *,
        icon: Optional[str] = None,
        block_color: Optional[Union[BlockColor, str]] = None,
    ) -> None:
        super().__init__()

        if not block_color:
            block_color = BlockColor.default

        self.set("type", "callout")
        self.nest("callout", "rich_text", rich_text)
        self.nest("callout", "color", block_color)
        if icon:
            self.nest("callout", "icon", ExternalFile(icon))


class QuoteBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[Union[RichText, Mention, Equation]],
        /,
        *,
        block_color: Optional[Union[BlockColor, str]] = None,
    ) -> None:
        super().__init__()

        if not block_color:
            block_color = BlockColor.default

        self.set("type", "quote")
        self.nest("quote", "rich_text", rich_text)
        self.nest("quote", "color", block_color)


class BulletedListItemBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[Union[RichText, Mention, Equation]],
        /,
        *,
        block_color: Optional[Union[BlockColor, str]] = None,
    ) -> None:
        super().__init__()

        if not block_color:
            block_color = BlockColor.default

        self.set("type", "bulleted_list_item")
        self.nest("bulleted_list_item", "rich_text", rich_text)
        self.nest("bulleted_list_item", "color", block_color)


class NumberedListItemBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[Union[RichText, Mention, Equation]],
        /,
        *,
        block_color: Optional[Union[BlockColor, str]] = None,
    ) -> None:
        super().__init__()

        if not block_color:
            block_color = BlockColor.default

        self.set("type", "numbered_list_item")
        self.nest("numbered_list_item", "rich_text", rich_text)
        self.nest("numbered_list_item", "color", block_color)


class ToDoBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[Union[RichText, Mention, Equation]],
        /,
        *,
        checked: Optional[bool] = False,
        block_color: Optional[Union[BlockColor, str]] = None,
    ) -> None:
        super().__init__()

        if not block_color:
            block_color = BlockColor.default

        self.set("type", "to_do")
        self.nest("to_do", "rich_text", rich_text)
        self.nest("to_do", "color", block_color)
        self.nest("to_do", "checked", checked)


class ToggleBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[Union[RichText, Mention, Equation]],
        /,
        *,
        block_color: Optional[Union[BlockColor, str]] = None,
    ) -> None:
        super().__init__()

        if not block_color:
            block_color = BlockColor.default

        self.set("type", "toggle")
        self.nest("toggle", "rich_text", rich_text)
        self.nest("toggle", "color", block_color)


class CodeBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[Union[RichText, Mention, Equation]],
        /,
        *,
        language: Optional[Union[CodeBlockLang, str]] = None,
        caption: Optional[Sequence[Union[RichText, Mention, Equation]]] = None,
    ) -> None:
        super().__init__()

        if not language:
            language = CodeBlockLang.plain_text

        self.set("type", "code")
        self.nest("code", "rich_text", rich_text)
        self.nest("code", "language", language)
        self.nest("code", "caption", caption) if caption else None


class EmbedBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, embedded_url: str, /) -> None:
        super().__init__()
        self.set("type", "embed")
        self.set("embed", NotionURL(embedded_url))


class BookmarkBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        bookmark_url: str,
        /,
        *,
        caption: Optional[Sequence[Union[RichText, Mention, Equation]]] = None,
    ) -> None:
        super().__init__()
        self.set("type", "bookmark")
        self.set("bookmark", NotionURL(bookmark_url))
        self.nest("bookmark", "caption", caption) if caption else None


class EquationBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, expression: str) -> None:
        super().__init__()
        self.set("type", "equation")
        self.nest("equation", "expression", expression)


class TableOfContentsBlocktype(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, block_color: Optional[Union[BlockColor, str]] = None) -> None:
        super().__init__()

        if not block_color:
            block_color = BlockColor.default

        self.set("type", "table_of_contents")
        self.nest("table_of_contents", "color", block_color)


class Heading1BlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[Union[RichText, Mention, Equation]],
        /,
        *,
        block_color: Optional[Union[BlockColor, str]] = None,
        is_toggleable: Optional[bool] = False,
    ) -> None:
        super().__init__()

        if not block_color:
            block_color = BlockColor.default

        self.set("type", "heading_1")
        self.nest("heading_1", "rich_text", rich_text)
        self.nest("heading_1", "color", block_color)
        self.nest("heading_1", "is_toggleable", is_toggleable)


class Heading2BlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[Union[RichText, Mention, Equation]],
        /,
        *,
        block_color: Optional[Union[BlockColor, str]] = None,
        is_toggleable: Optional[bool] = False,
    ) -> None:
        super().__init__()

        if not block_color:
            block_color = BlockColor.default

        self.set("type", "heading_2")
        self.nest("heading_2", "rich_text", rich_text)
        self.nest("heading_2", "color", block_color)
        self.nest("heading_2", "is_toggleable", is_toggleable)


class Heading3BlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        rich_text: Sequence[Union[RichText, Mention, Equation]],
        /,
        *,
        block_color: Optional[Union[BlockColor, str]] = None,
        is_toggleable: Optional[bool] = False,
    ) -> None:
        super().__init__()

        if not block_color:
            block_color = BlockColor.default

        self.set("type", "heading_3")
        self.nest("heading_3", "rich_text", rich_text)
        self.nest("heading_3", "color", block_color)
        self.nest("heading_3", "is_toggleable", is_toggleable)


class LinkToPageBlockType(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, page_id: str) -> None:
        super().__init__()

        self.set("type", "link_to_page")
        self.nest("link_to_page", "type", "page_id")
        self.nest("link_to_page", "page_id", page_id)


class BreadcrumbBlock(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self) -> None:
        super().__init__()
        self.set("type", "breadcrumb")
        self.set("breadcrumb", {})


class DividerBlock(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self) -> None:
        super().__init__()
        self.set("type", "divider")
        self.set("divider", {})
