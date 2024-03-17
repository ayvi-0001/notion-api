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

from typing import Sequence

from notion.properties import files, options
from notion.properties.common import BotObject, Parent, UserObject
from notion.properties.files import ExternalFile, InternalFile
from notion.properties.options import (
    BlockColor,
    CodeBlockLang,
    FunctionFormat,
    NumberFormat,
    PropertyColor,
)
from notion.properties.propertyobjects import Option
from notion.properties.richtext import Annotations, Equation, Mention, RichText

__all__: Sequence[str] = (
    "files",
    "options",
    "BotObject",
    "Parent",
    "UserObject",
    "RichText",
    "Annotations",
    "Mention",
    "Equation",
    "Option",
    "BlockColor",
    "PropertyColor",
    "CodeBlockLang",
    "FunctionFormat",
    "NumberFormat",
    "ExternalFile",
    "InternalFile",
)
