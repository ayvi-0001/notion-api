"""
File objects contain data about a file that is uploaded to Notion, or data about an external file that is linked to in Notion.
Page, embed, image, video, file, pdf, and bookmark block types all contain file objects. 
Icon and cover page object values also contain file objects.
"""
from __future__ import annotations
import typing

from notion.core import build
from notion.properties.richtext import RichText
from notion.properties.common import NotionURL
from notion.core.typedefs import PagePropertyValue

__all__: typing.Sequence[str] = (
    "FilesPropertyValue", 
    "Icon", 
    "Emoji", 
    "ExternalFile", 
    "InternalFile"
    )

# TODO emoji
# TODO cover

class FilesPropertyValue(build.NotionObject, PagePropertyValue):
    """When updating a file property, the value is overwritten by the array of files passed.
    Although Notion doesn't support uploading files, if you pass a file object containing a file hosted by Notion, 
    it remains one of the files. To remove any file, just don't pass it in the update response.
    ---
    InternalFiles are a file object corresponding to a file that has been uploaded to Notion.
    ExternalFiles are a file object corresponding to an external file that has been linked to in Notion.
    ---
    (required)
    :param array_of_files: An array of objects containing information about the files.
                           Either InternalFile(), ExternalFile() or a combination of both.
    ---
    (optional)
    :param property_name: Adds a `name` key with the input property name, and a `name` attribute
                          to be used with `notion.properties.PropertySchema` to set the `name` as the first key.
                          (Required for certain page/database endpoints.)
    ---
    https://developers.notion.com/reference/page-property-values#files
    """
    __slots__: typing.Sequence[str] = ('name')

    def __init__(self, array_of_files: list[InternalFile | ExternalFile], /, *, property_name: str | None = None) -> None:
        super().__init__()
        if property_name:
            self.name = property_name
            self.set('name', self.name)

        self.set('type', 'files')
        self.set('files', array_of_files)


class Icon(build.NotionObject):
    def __init__(self, file_type: typing.Literal['internal', 'external'], file_url: str, /) -> None:
        super().__init__()

        _icon = build.NotionObject()
        if file_type == 'internal':
            _icon = InternalFile(file_url)
        if file_type == 'external':
            _icon = InternalFile(file_url)

        self.set('icon', _icon)


class Emoji(build.NotionObject):
    """https://developers.notion.com/reference/emoji-object"""
    def __init__(self, emoji_character, /) -> None:
        super().__init__()

        self.set('type', 'emoji')
        self.set('emoji', emoji_character)


class ExternalFile(build.NotionObject):
    """The Notion API supports adding, retrieving, and updating links to external files.
    The name of the file. For "external" file objects, the name is the same as the file's host URL.
    
    ---
    https://developers.notion.com/reference/file-object#external-files
    """
    def __init__(self, url, /, *, name: str | None = None, caption: list[RichText] | None = None) -> None:
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
    def __init__(self, url, /, *, name: str | None = None, caption: list[RichText] | None = None) -> None:
        super().__init__()

        self.set('type', 'file')    
        self.set('file', NotionURL(url))
        self.set('name', name) if name else None
        self.set('caption', caption) if caption else None
