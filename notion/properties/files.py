"""
File objects contain data about a file that is uploaded to Notion, or data about an external file that is linked to in Notion.
Page, embed, image, video, file, pdf, and bookmark block types all contain file objects. 
Icon and cover page object values also contain file objects.
"""
from __future__ import annotations
from typing import Sequence
from typing import Union
from typing import Optional

from notion.core import build
from notion.properties.richtext import RichTextTypeObject
from notion.properties.common import NotionURL
from notion.core.typedefs import PagePropertyValue

__all__: Sequence[str] = (
    "Icon", 
    "ExternalFile", 
    "InternalFile",
    "FilesPropertyValue", 
)

# TODO cover
# TODO Emoji

class FilesPropertyValue(PagePropertyValue, build.NotionObject):
    """When updating a file property, the value is overwritten by the array of files passed.
    Although Notion doesn't support uploading files, if you pass a file object containing a file hosted by Notion, 
    it remains one of the files. To remove any file, just don't pass it in the update response.

    InternalFiles are a file object corresponding to a file that has been uploaded to Notion.
    ExternalFiles are a file object corresponding to an external file that has been linked to in Notion.

    ---
    :param array_of_files: (required) An array of objects containing information about the files. \
        Either InternalFile(), ExternalFile() or a combination of both.

    ---
    https://developers.notion.com/reference/page-property-values#files
    """
    __slots__: Sequence[str] = ('name')

    def __init__(self, property_name: str, 
                 array_of_files: list[Union[InternalFile, ExternalFile]]) -> None:
        super().__init__(property_name=property_name)
        self.set('type', 'files')
        self.set('files', array_of_files)


# Internal file type Icons currently not supported.
class Icon(build.NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, file_url: str, /) -> None:
        super().__init__()
        self.set('type', 'icon')
        self.set('icon', ExternalFile(file_url))


class ExternalFile(build.NotionObject):
    """The Notion API supports adding, retrieving, and updating links to external files.
    The name of the file. For "external" file objects, the name is the same as the file's host URL.
    
    ---
    https://developers.notion.com/reference/file-object#external-files
    """
    __slots__: Sequence[str] = ()

    def __init__(self, url, /, *, 
                 name: Optional[str] = None, 
                 caption: Optional[RichTextTypeObject] = None) -> None:
        super().__init__()
        self.set('type', 'external')            
        self.set('external', NotionURL(url))
        self.set('name', name) if name else None
        self.set('caption', caption) if caption else None


class InternalFile(build.NotionObject):
    """You can retrieve links to Notion-hosted files via the Retrieve block children endpoint.
    
    ---
    https://developers.notion.com/reference/file-object#notion-hosted-files
    """
    __slots__: Sequence[str] = ()
    
    def __init__(self, url, /, *, 
                 name: Optional[str] = None, 
                 caption: Optional[RichTextTypeObject] = None) -> None:
        super().__init__()
        self.set('type', 'file')    
        self.set('file', NotionURL(url))
        self.set('name', name) if name else None
        self.set('caption', caption) if caption else None
