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
File objects contain data about a file that is uploaded to Notion, or data about an external file that is linked to in Notion.
Page, embed, image, video, file, pdf, and bookmark block types all contain file objects. 
Icon and cover page object values also contain file objects.

A file with type `file` must contain a Notion hosted file url. Use type `external` for externally hosted files.
"""
from __future__ import annotations

from typing import Optional, Sequence

from notion.properties.build import NotionObject
from notion.properties.common import _NotionURL
from notion.properties.propertyvalues import PagePropertyValue
from notion.properties.richtext import Mention, RichText

__all__: Sequence[str] = (
    "Icon",
    "Cover",
    "ExternalFile",
    "InternalFile",
    "FilesPropertyValue",
)


class FilesPropertyValue(PagePropertyValue, NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(
        self, property_name: str, array_of_files: Sequence[InternalFile | ExternalFile]
    ) -> None:
        """
        When updating a file property, the value is overwritten by the array of files passed.
        Although Notion doesn't support uploading files, if you pass a file object containing a file hosted by Notion,
        it remains one of the files. To remove any file, just don't pass it in the update response.

        InternalFiles are a file object corresponding to a file that has been uploaded to Notion.
        ExternalFiles are a file object corresponding to an external file that has been linked to in Notion.

        ---
        :param array_of_files: (required) An array of objects containing information about the files.\
                                Either InternalFile(), ExternalFile() or a combination of both.

        https://developers.notion.com/reference/page-property-values#files
        """
        super().__init__(property_name=property_name)
        self.set("type", "files")
        self.set("files", array_of_files)


class Icon(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, file_url: str, /) -> None:
        """
        Internal object for setting the icon of a page.
        Internal file type Icons currently not supported.
        """
        super().__init__()
        self.set("icon", ExternalFile(file_url))


class Cover(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, file_url: str, /) -> None:
        """
        Internal object for setting the cover of a page.
        Internal file type covers currently not supported.
        """
        super().__init__()
        self.set("cover", ExternalFile(file_url))


class ExternalFile(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self, url: str, /, *, caption: Optional[Sequence[RichText | Mention]] = None
    ) -> None:
        """
        The Notion API supports adding, retrieving, and updating links to external files.
        For "external" file objects, the name is the same as the file's host URL.

        https://developers.notion.com/reference/file-object#external-files
        """
        super().__init__()
        self.set("type", "external")
        self.set("external", _NotionURL(url))
        self.set("caption", caption) if caption else None


class InternalFile(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        name: str,
        url: str,
        *,
        caption: Optional[Sequence[RichText | Mention]] = None,
    ) -> None:
        """
        Internal files are any files hosted on Notion
        They begin with: https://s3.{region}.amazonaws.com/secure.notion-static.com/{block_id}/...
        You can retrieve links to Notion-hosted files via the Retrieve block children endpoint.

        https://developers.notion.com/reference/file-object#notion-hosted-files
        """
        super().__init__()
        self.set("type", "file")
        self.set("file", _NotionURL(url))
        self.set("name", name) if name else None
        self.set("caption", caption) if caption else None
