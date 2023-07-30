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
#### Main Objects:
>>> notion.Page | notion.Database | notion.Block | notion.Workspace

#### PropertyItems:
>>> from notion import propertyitems

#### Queries:
>>> from notion import query

#### Properties:
>>> from notion import properties as prop

#### Block Extensions:
>>> notion.CodeBlock | notion.ToDoBlock | notion.EquationBlock | notion.RichTextBlock

"""
from typing import Sequence

from notion.api import Block, Database, Page, Workspace
from notion.api._pkgv import check_for_pkg_update
from notion.api.block_ext import (
    CodeBlock,
    EquationBlock,
    RichTextBlock,
    TableBlock,
    ToDoBlock,
)

__all__: Sequence[str] = (
    "Page",
    "Database",
    "Block",
    "Workspace",
    "CodeBlock",
    "EquationBlock",
    "ToDoBlock",
    "RichTextBlock",
    "TableBlock",
    "check_for_pkg_update",
)
