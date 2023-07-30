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

from typing import Any, MutableMapping, Optional, Sequence, cast

from notion.api.blockmixin import _TokenBlockMixin
from notion.properties.options import BlockColor
from notion.properties.richtext import Annotations, RichText

__all__: Sequence[str] = ["RichTextBlock"]

TEXT_EDITABLE_BLOCKS = [
    "paragraph",
    "to_do",
    "heading_1",
    "heading_2",
    "heading_3",
    "bulleted_list_item",
    "numbered_list_item",
    "toggle",
    "quote",
    "callout",
]


class RichTextBlock(_TokenBlockMixin):
    """For text-editable blocks containing a rich_text key.
    Added properties/setters to retrieve/set: text, href, annotatations

    Blocks with editable text:
    "paragraph", "to_do", "toggle", "quote", "callout"
    "bulleted_list_item", "numbered_list_item",
    "headings", "toggle_headings"

    Use clear_text() to clear the text of the block.
    Use clear_annotations() to clear the annotations of the block.
    """

    def __init__(self, id: str, /, *, token: Optional[str] = None) -> None:
        super().__init__(id, token=token)

        if set([self.type]).isdisjoint(TEXT_EDITABLE_BLOCKS):
            raise TypeError(f"Block type must be one of {TEXT_EDITABLE_BLOCKS}.")

    @property
    def text(self) -> str:
        block = self._block[self.type]

        try:
            if len(block["rich_text"]) > 1:
                text = []
                for rc in block["rich_text"]:
                    text.append(rc["text"]["content"])

                return "".join(text)

            else:
                text = self._block[self.type]["rich_text"][0]["text"]["content"]
                return cast(str, text)
        except IndexError:
            return ""

    def set_text(self, value: Sequence[RichText]) -> None:
        text = self._block
        text.pop(self.type)
        text |= {self.type: {"rich_text": value}}
        self._patch(self._block_endpoint(self.id), payload=text)

    @property
    def href(self) -> str:
        try:
            href = cast(str, self._block[self.type]["rich_text"][0]["href"])
        except IndexError:
            return ""

        return href

    @href.setter
    def href(self, url: str) -> None:
        text = self._block[self.type]
        if text["rich_text"]:
            text["rich_text"][0]["href"] = url
            self._patch(self._block_endpoint(self.id), payload={self.type: text})

    def annotate(
        self,
        bold: Optional[bool] = None,
        italic: Optional[bool] = None,
        strikethrough: Optional[bool] = None,
        underline: Optional[bool] = None,
        code: Optional[bool] = None,
        color: Optional[BlockColor | str] = None,
    ) -> None:
        text = self._block[self.type]
        annotations = Annotations(
            bold=bold,
            italic=italic,
            strikethrough=strikethrough,
            underline=underline,
            code=code,
            color=color,
        )
        text["rich_text"][0]["annotations"] = annotations
        self._patch(self._block_endpoint(self.id), payload={self.type: text})

    def clear_text(self) -> None:
        self.set_text([RichText("")])

    def clear_annotations(self) -> None:
        self.annotate()
