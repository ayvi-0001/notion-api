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
File objects contain data about a file that is uploaded to Notion, or data about an external file that is linked to in Notion.
Page, embed, image, video, file, pdf, and bookmark block types all contain file objects. 
Icon and cover page object values also contain file objects.

A file with type `file` must contain a Notion hosted file url. Use type `external` for externally hosted files.
"""
from __future__ import annotations
from typing import Sequence
from typing import Union
from typing import Optional

from notion.core import build
from notion.properties.common import NotionURL
from notion.core.typedefs import PagePropertyValue
from notion.properties.richtext import RichTextTypeObject

__all__: Sequence[str] = (
    "Icon",
    "ExternalFile",
    "InternalFile",
    "FilesPropertyValue",
)

# TODO cover


class FilesPropertyValue(PagePropertyValue, build.NotionObject):
    """When updating a file property, the value is overwritten by the array of files passed.
    Although Notion doesn't support uploading files, if you pass a file object containing a file hosted by Notion, 
    it remains one of the files. To remove any file, just don't pass it in the update response.

    InternalFiles are a file object corresponding to a file that has been uploaded to Notion.
    ExternalFiles are a file object corresponding to an external file that has been linked to in Notion.

    ---
    :param array_of_files: (required) An array of objects containing information about the files. \
        Either InternalFile(), ExternalFile() or a combination of both.

    https://developers.notion.com/reference/page-property-values#files
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(
        self,
        property_name: str,
        array_of_files: list[Union[InternalFile, ExternalFile]],
    ) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "files")
        self.set("files", array_of_files)


# Internal file type Icons currently not supported.
class Icon(build.NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, file_url: str, /) -> None:
        super().__init__()
        self.set("icon", ExternalFile(file_url))


class ExternalFile(build.NotionObject):
    """The Notion API supports adding, retrieving, and updating links to external files.
    The name of the file. For "external" file objects, the name is the same as the file's host URL.

    https://developers.notion.com/reference/file-object#external-files
    """

    __slots__: Sequence[str] = ()

    def __init__(
        self, url: str, /, *, caption: Optional[RichTextTypeObject] = None
    ) -> None:
        super().__init__()
        self.set("type", "external")
        self.set("external", NotionURL(url))
        self.set("caption", caption) if caption else None


class InternalFile(build.NotionObject):
    """
    Internal files are any files hosted on Notion, and will begin with:
        https://s3.us-west-2.amazonaws.com/secure.notion-static.com/{block_id}/...

    You can retrieve links to Notion-hosted files via the Retrieve block children endpoint.

    https://developers.notion.com/reference/file-object#notion-hosted-files
    """

    __slots__: Sequence[str] = ()

    def __init__(
        self, name: str, url: str, *, caption: Optional[RichTextTypeObject] = None
    ) -> None:
        super().__init__()
        self.set("type", "file")
        self.set("file", NotionURL(url))
        self.set("name", name) if name else None
        self.set("caption", caption) if caption else None
