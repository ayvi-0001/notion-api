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

from typing import Optional, Sequence

from notion.api.block_ext.richtext import RichTextBlock

__all__: Sequence[str] = ("ToDoBlock",)


class ToDoBlock(RichTextBlock):
    def __init__(self, id: str, /, *, token: Optional[str] = None) -> None:
        super().__init__(id, token=token)

        if self.type != "to_do":
            raise TypeError(
                f"Block type must be 'to_do', not '{self.type}' for ToDoBlock."
            )

    @property
    def checked(self) -> bool:
        checked: bool = self._block["to_do"]["checked"]
        return checked

    @checked.setter
    def checked(self, value: bool) -> None:
        checked = self._block["to_do"]
        checked["checked"] = value
        self._patch(self._block_endpoint(self.id), payload={self.type: checked})
