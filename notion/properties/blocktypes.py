""" 
A block object represents content within Notion. Blocks can be text, lists, media, and more. A page is a type of block, too.
Some blocks have more content nested inside them. Some examples are indented paragraphs, lists, and toggles. 
The nested content is called children, and children are blocks, too.

Block types that support children
Block types which support children are:
    "paragraph", "bulleted_list_item", "numbered_list_item", "toggle", "to_do", "quote", "callout", 
    "synced_block", "template", "column", "child_page", "child_database", and "table". 
    All heading blocks ("heading_1", "heading_2", and "heading_3") support children when the is_toggleable property is true.
---
https://developers.notion.com/reference/block
"""
from __future__ import annotations
import typing

from notion.core import build
from notion.core.typedefs import BlockTypeObjects
from notion.properties.files import Icon
from notion.properties.files import Emoji
from notion.properties.files import InternalFile
from notion.properties.files import ExternalFile
from notion.properties.common import NotionURL
from notion.properties.options import CodeEnum
from notion.properties.options import ColorEnum
from notion.properties.pagepropertyvalues import RichTextPropertyValue

__all__: typing.Sequence[str] = (
    "Children", 
    "Caption", 
    "OriginalSyncedBlockType", 
    "ReferenceSyncedBlockType", 
    "ParagraphBlocktype", 
    # "HeadingOneBlocktype", 
    # "HeadingTwoBlocktype", 
    # "HeadingThreeBlocktype", 
    "CalloutBlocktype", 
    "QuoteBlocktype", 
    "BulletedListItemBlocktype", 
    "NumberedListItemBlocktype", 
    "ToDoBlocktype", 
    "ToggleBlocktype", 
    "CodeBlocktype", 
    "ChildPageBlocktype", 
    "ChildDatabaseBlocktype", 
    "EmbedBlocktype", 
    "ImageBlocktype", 
    "VideoBlocktype", 
    "FileBlocktype", 
    "PdfBlocktype", 
    "BookmarkBlocktype", 
    "EquationBlocktype", 
    "DividerBlocktype", 
    "TableOfContentsBlocktype", 
    "BreadcrumbBlocktype", 
    # "ColumnList", 
    # "ColumnBlocktype", 
    # "LinkPreviewBlocktype", 
    # "TemplateBlocktype", 
    # "LinkToPageBlocktype", 
    # "TableBlocktype", 
    # "TableRowBlocktype"
)


class Children(build.NotionObject):
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, array_of_block_type_objects: list[BlockTypeObjects]) -> None:
        super().__init__()

        self.set('children', array_of_block_type_objects)


class Caption(build.NotionObject):
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, rich_text_property: RichTextPropertyValue) -> None:
        super().__init__()

        self.set('caption', rich_text_property)



class OriginalSyncedBlockType(build.NotionObject, BlockTypeObjects): 
    """Similar to the UI, there are two versions of a synced_block -- 
    the original block that was created first and doesn't yet sync with anything else, 
    and the reference blocks that are synced to the original synced block.
    
    ### Original Synced Block
    To create a synced_block, the developer needs to create an original synced block. 
    Developers will be able to identify the original synced_block because it does not 
    "sync_from" any other block (synced_from property is set to null).
    
    Note that all of the blocks available to be synced in another synced_block must be captured in the children property.
    
    ---
    :param synced_from: Value is always null to signify that this is an original synced block and that is not referring to another block
    :param children: Any nested children blocks of the synced_block block. 
                     These blocks will be synced across this block and references to this synced_block
    ---
    https://developers.notion.com/reference/block#synced-block-blocks
    """
    __slots__: typing.Sequence[str] = ('_synced_block')

    def __init__(self, children: Children) -> None:
        super().__init__()

        self._synced_block = build.NotionObject()
        self._synced_block.set('synced_from', None)
        self._synced_block.set('children', children)

        self.set('type', 'synced_block')
        self.set('synced_block', self._synced_block)


class ReferenceSyncedBlockType(build.NotionObject, BlockTypeObjects): 
    """    
    ### Reference Synced Block
    To sync the content of the original synced_block with another synced_block, 
    the developer simply needs to refer to that synced_block using the synced_from property.
    
    Note that only "original" synced blocks can be referenced in the synced_from property.
    
    ---
    :param block_id: (required) string (UUIDv4). Identifier of an original synced_block
    :param synced_from: Type: Synced From Object. Object that contains the id of the original synced_block
    
    ---
    https://developers.notion.com/reference/block#synced-block-blocks
    """
    __slots__: typing.Sequence[str] = ('_synced_from', '_synced_block')

    def __init__(self, block_id: str) -> None:
        super().__init__()

        self._synced_block = build.NotionObject()
        self._synced_block.set('type', 'block_id')
        self._synced_block.set('block_id', block_id)

        self._synced_from = build.NotionObject()
        self._synced_from.set('synced_from', self._synced_block)

        self.set('type', 'synced_block')
        self.set('synced_block', self._synced_from)


class ParagraphBlocktype(build.NotionObject, BlockTypeObjects):
    """
    (required)
    :param rich_text_object: A single RichText object in the paragraph block.
    ---
    (optional)
    :param children: Array of block objects. Any nested children blocks of the paragraph block.
    :param color: Color of the block. `notion.properties.options.ColorEnum`.
    ---
    https://developers.notion.com/reference/block#paragraph-blocks
    """
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, rich_text_object: RichTextPropertyValue, children: list[BlockTypeObjects] | None = None, 
                 /, *, block_color: ColorEnum | str | None = ColorEnum.default.value) -> None:
        super().__init__()

        self.set('type', 'paragraph')
        self.set('paragraph', rich_text_object)
        self.set('color', block_color)
        self.set('children', children) if children else None


# class HeadingOneBlocktype(build.NotionObject, BlockTypeObjects): 
#     __slots__: typing.Sequence[str] = ()
    
#     def __init__(self) -> None:
#         super().__init__()


# class HeadingTwoBlocktype(build.NotionObject, BlockTypeObjects): 
#     __slots__: typing.Sequence[str] = ()
    
#     def __init__(self) -> None:
#         super().__init__()


# class HeadingThreeBlocktype(build.NotionObject, BlockTypeObjects): 
#     __slots__: typing.Sequence[str] = ()
    
#     def __init__(self) -> None:
#         super().__init__()


class CalloutBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#callout-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, 
                 rich_text_object: RichTextPropertyValue, 
                 children: list[BlockTypeObjects] | None = None, 
                 /, *, 
                 icon: Icon | Emoji | None = None, 
                 block_color: ColorEnum | str | None = ColorEnum.default.value) -> None:
        super().__init__()

        self.set('type', 'callout')
        self.set('callout', rich_text_object)
        self.set('color', block_color)
        self.set('icon', icon) if icon else None
        self.set('children', children) if children else None


class QuoteBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#quote-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, rich_text_object: RichTextPropertyValue, children: list[BlockTypeObjects] | None = None, 
                 /, *, block_color: ColorEnum | str | None = ColorEnum.default.value) -> None:
        super().__init__()

        self.set('type', 'quote')
        self.set('quote', rich_text_object)
        self.set('color', block_color)
        self.set('children', children) if children else None


class BulletedListItemBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#bulleted-list-item-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, rich_text_object: RichTextPropertyValue, children: list[BlockTypeObjects] | None = None, 
                 /, *, block_color: ColorEnum | str | None = ColorEnum.default.value) -> None:
        super().__init__()

        self.set('type', 'bulleted_list_item')
        self.set('bulleted_list_item', rich_text_object)
        self.set('color', block_color)
        self.set('children', children) if children else None


class NumberedListItemBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#numbered-list-item-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, rich_text_object: RichTextPropertyValue, children: list[BlockTypeObjects] | None = None, 
                 /, *, block_color: ColorEnum | str | None = ColorEnum.default.value) -> None:
        super().__init__()

        self.set('type', 'numbered_list_item')
        self.set('numbered_list_item', rich_text_object)
        self.set('color', block_color)
        self.set('children', children) if children else None


class ToDoBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#to-do-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, 
                 rich_text_object: RichTextPropertyValue, 
                 checked: bool | None = None, 
                 children: list[BlockTypeObjects] | None = None, 
                 /, *, 
                 block_color: ColorEnum | str | None = ColorEnum.default.value) -> None:
        super().__init__()

        self.set('type', 'to_do')
        self.set('to_do', rich_text_object)
        self.set('color', block_color)
        self.set('checked', checked) if checked else None
        self.set('children', children) if children else None


class ToggleBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#toggle-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, rich_text_object: RichTextPropertyValue, children: list[BlockTypeObjects] | None = None, 
                 /, *, block_color: ColorEnum | str | None = ColorEnum.default.value) -> None:
        super().__init__()

        self.set('type', 'toggle')
        self.set('toggle', rich_text_object)
        self.set('color', block_color)
        self.set('children', children) if children else None


class CodeBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#code-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, 
                 rich_text_object: RichTextPropertyValue, 
                 /, *, 
                 caption: Caption | None = None, 
                 language: CodeEnum | None = None) -> None:
        super().__init__()

        self.set('type', 'code')
        self.set('code', rich_text_object)
        self.set('caption', caption) if caption else None
        self.set('language', language) if language else None


class ChildPageBlocktype(build.NotionObject, BlockTypeObjects):
    """Creating and Updating child_pages:

    To create or update child_page type blocks, use the Create Page and the Update page endpoint.
    ---
    https://developers.notion.com/reference/block#child-page-blocks
    """ 
    __slots__: typing.Sequence[str] = ('_page_title')
    
    def __init__(self, page_title: str, /) -> None:
        super().__init__()

        self._page_title = build.NotionObject()
        self._page_title.set('title', page_title)
        
        self.set('type', 'child_page')
        self.set('child_page', self._page_title)


class ChildDatabaseBlocktype(build.NotionObject, BlockTypeObjects):
    """Creating and Updating child_databases:

    To create or update child_database type blocks, use the Create Page and the Update page endpoint.
    ---
    https://developers.notion.com/reference/block#child-database-blocks
    """ 
    __slots__: typing.Sequence[str] = ('_database_title')
    
    def __init__(self, database_title: str, /) -> None:
        super().__init__()

        self._database_title = build.NotionObject()
        self._database_title.set('title', database_title)
        
        self.set('type', 'child_database')
        self.set('child_database', self._database_title)


class EmbedBlocktype(build.NotionObject, BlockTypeObjects): 
    """
    Embed block types are:
    Framer, Twitter (tweets), Google Drive documents, Gist, Figma, 
    Invision, Loom, Typeform, Codepen, PDFs, Google Maps, Whimisical, 
    Miro, Abstract, excalidraw, Sketch, Replit
    There is no need to specify the specific embed type, only the URL.

    ### Differences in embed blocks between the Notion app and the API
    The Notion app uses a 3rd-party service, Embedly, to validate and request metadata for embeds given a URL. 
    This works well in a web app because Notion can kick off an asynchronous request for URL information, 
    which might take seconds or longer to complete, and then update the block with the metadata in the UI 
    after receiving a response from Embedly.

    Embedly is not called when creating embed blocks in the API because the API needs to be able to return 
    faster than the UI, and because the response from Embedly could actually cause us change the block type. 
    This would result in a slow and potentially confusing experience as the block in the response would 
    not match the block sent in the request.
    The result is that embed blocks created via the API may not look exactly like their counterparts created in the Notion app.

    ---
    https://developers.notion.com/reference/block#embed-blocks
    """
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, embedded_url: str, /) -> None:
        super().__init__()

        self.set('type', 'embed')
        self.set('embed', NotionURL(embedded_url))

class ImageBlocktype(build.NotionObject, BlockTypeObjects): 
    """Includes supported image urls 
    (i.e. ending in .png, .jpg, .jpeg, .gif, .tif, .tiff, .bmp, .svg, or .heic). 
    Note that the url property only accepts direct urls to an image. 
    The image must be directly hosted. 
    In other words, the url cannot point to a service that retrieves the image.
    
    ---
    https://developers.notion.com/reference/block#image-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, image: InternalFile | ExternalFile, /) -> None:
        super().__init__()

        self.set('type', 'image')
        self.set('image', image)


class VideoBlocktype(build.NotionObject, BlockTypeObjects): 
    """Includes supported video urls 
    (e.g. ending in .mkv, .flv, .gifv, .avi, .mov, .qt, .wmv, 
        .asf, .amv, .mp4, .m4v, .mpeg, .mpv, .mpg, .f4v, etc.)

    ---
    https://developers.notion.com/reference/block#video-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, video: InternalFile | ExternalFile, /) -> None:
        super().__init__()

        self.set('type', 'video')
        self.set('video', video)

class FileBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#file-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, file: InternalFile | ExternalFile, /, *, caption: Caption) -> None:
        super().__init__()

        self.set('type', 'file')
        self.set('file', file)
        self.set('caption', caption) if caption else None


class PdfBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#pdf-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, pdf: InternalFile | ExternalFile, /) -> None:
        super().__init__()

        self.set('type', 'pdf')
        self.set('pdf', pdf)

class BookmarkBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#bookmark-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self, bookmark: str, /, *, caption: Caption) -> None:
        super().__init__()

        self.set('type', 'bookmark')
        self.set('bookmark', NotionURL(bookmark))
        self.set('caption', caption) if caption else None


class EquationBlocktype(build.NotionObject, BlockTypeObjects): 
    """
    (required)
    :param expression: A KaTeX compatible string
    ---
    https://developers.notion.com/reference/block#equation-blocks"""
    __slots__: typing.Sequence[str] = ('_expression')
    
    def __init__(self, expression: str) -> None:
        super().__init__()

        self._expression = build.NotionObject()
        self._expression.set('expression', expression)

        self.set('type', 'equation')
        self.set('equation', self._expression)


class DividerBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#divider-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self) -> None:
        super().__init__()

        self.set('type', 'divider')
        self.set('divider', {})


class TableOfContentsBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#table-of-contents-blocks"""
    __slots__: typing.Sequence[str] = ('_color')
    
    def __init__(self, color: ColorEnum | str | None = ColorEnum.default.value) -> None:
        super().__init__()
        
        self._color = build.NotionObject()
        self._color.set('color', color)

        self.set('type', 'table_of_contents')
        self.set('table_of_contents', self._color)


class BreadcrumbBlocktype(build.NotionObject, BlockTypeObjects): 
    """https://developers.notion.com/reference/block#breadcrumb-blocks"""
    __slots__: typing.Sequence[str] = ()
    
    def __init__(self) -> None:
        super().__init__()

        self.set('type', 'breadcrumb')
        self.set('breadcrumb', {})


# class ColumnList(build.NotionObject, BlockTypeObjects): 
#     __slots__: typing.Sequence[str] = ()
    
#     def __init__(self) -> None: 
#         super().__init__()

# class ColumnBlocktype(build.NotionObject, BlockTypeObjects): 
#     __slots__: typing.Sequence[str] = ()
    
#     def __init__(self) -> None: 
#         super().__init__()


# class LinkPreviewBlocktype(build.NotionObject, BlockTypeObjects): 
#     __slots__: typing.Sequence[str] = ()
    
#     def __init__(self) -> None:
#         super().__init__()


# class TemplateBlocktype(build.NotionObject, BlockTypeObjects): 
#     __slots__: typing.Sequence[str] = ()
    
#     def __init__(self) -> None:
#         super().__init__()


# class LinkToPageBlocktype(build.NotionObject, BlockTypeObjects): 
#     __slots__: typing.Sequence[str] = ()
    
#     def __init__(self) -> None:
#         super().__init__()


# class TableBlocktype(build.NotionObject, BlockTypeObjects): 
#     __slots__: typing.Sequence[str] = ()
    
#     def __init__(self) -> None:
#         super().__init__


# class TableRowBlocktype(build.NotionObject, BlockTypeObjects): 
#     __slots__: typing.Sequence[str] = ()
    
#     def __init__(self) -> None:
#         super().__init__
