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

from notion.api.blockmixin import _TokenBlockMixin

__all__: Sequence[str] = ("EquationBlock",)


class EquationBlock(_TokenBlockMixin):
    def __init__(self, id: str, /, *, token: Optional[str] = None) -> None:
        super().__init__(id, token=token)

        if self.type != "equation":
            raise TypeError(
                f"Block type must be 'equation', not '{self.type}' for EquationBlock."
            )

    def __repr__(self) -> str:
        return f'notion.EquationBlock("{getattr(self, "id", "")}")'

    @property
    def expression(self) -> str:
        return f"{self._block['equation']['expression']}"

    @expression.setter
    def expression(self, value: str) -> None:
        equation = self._block["equation"]
        equation["expression"] = value
        self._patch(self._block_endpoint(self.id), payload={self.type: equation})
