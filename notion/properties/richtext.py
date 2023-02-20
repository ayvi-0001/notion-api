"""
Rich text objects contain the data that Notion uses to display 
formatted text,mentions, and inline equations. 
Arrays of rich text objects within database property objects and page property value objects 
are used to create what a user experiences as a single text value in Notion.
"""
from __future__ import annotations
import typing

from notion.core import build 
from notion.properties.user import UserObject
from notion.properties.options import NotionColors
from notion.properties.common import NotionURL
from notion.properties.common import NotionUUID

__all__: typing.Sequence[str] = (
    "Annotations",
    "RichText",
    "Equation",
    "Mention",
)


class RichText(build.NotionObject):
    __slots__: typing.Sequence[str] = ()

    def __init__(self, content: str | None = None, /, annotations: Annotations | None = None, 
                 *, link: str | None = None) -> None:
        super().__init__()
        self.set('type', 'text')
        self.nest('text', 'content', content)
        self.nest('text', 'link', NotionURL(link)) if link else None
        if annotations is not None and annotations != {}:
            self.set('annotations', annotations)


class Equation(build.NotionObject):
    __slots__: typing.Sequence[str] = ()

    def __init__(self, expression: str, /, *, annotations: Annotations | None = None) -> None:
        super().__init__()
        self.set('type', 'equation')
        self.nest('equation', 'expression', expression)
        if annotations is not None and annotations != {}:
            self.set('annotations', annotations)


class Mention(build.NotionObject):
    __slots__: typing.Sequence[str] = ()

    def __init__(self, /, *, annotations: Annotations | None = None,
                 _mention_object: typing.Any | None = None, ) -> None:
        super().__init__()
        self.set('type', 'mention')
        self.set('mention', _mention_object)
        if annotations is not None and annotations != {}:
            self.set('annotations', annotations)
    
    @classmethod
    def user(cls, user_object: UserObject, /, *, annotations: Annotations | None = None):
        """ Cannot mention Bots
        :raises: `notion.exceptions.errors.NotionValidationError`: Content creation Failed."""
        return cls(_mention_object=user_object, annotations=annotations)

    @classmethod
    def link(cls, url, /, *, annotations: Annotations | None = None):
        link_preview = build.NotionObject()
        link_preview.set('type', 'link_preview')
        link_preview.nest('link_preview', 'url', url)
        return cls(_mention_object=link_preview, annotations=annotations)

    @classmethod
    def page(cls, id, /, *, annotations: Annotations | None = None):
        page = build.NotionObject()
        page.set('type', 'page')
        page.set('page', NotionUUID(id))
        return cls(_mention_object=page, annotations=annotations)
   
    @classmethod
    def database(cls, id, /, *, annotations: Annotations | None = None):
        database = build.NotionObject()
        database.set('type', 'database')
        database.set('database', NotionUUID(id))
        return cls(_mention_object=database, annotations=annotations)

    @classmethod
    def today(cls, /, *, annotations: Annotations | None = None):
        today = build.NotionObject()
        today.set('type', 'template_mention')
        today.nest('template_mention', 'type', 'template_mention_date')
        today.nest('template_mention', 'template_mention_date', 'today')
        return cls(_mention_object=today, annotations=annotations)

    @classmethod
    def now(cls, /, *, annotations: Annotations | None = None):
        now = build.NotionObject()
        now.set('type', 'template_mention')
        now.nest('template_mention', 'type', 'template_mention_date')
        now.nest('template_mention', 'template_mention_date', 'now')
        return cls(_mention_object=now, annotations=annotations)

    @classmethod
    def me(cls, /, *, annotations: Annotations | None = None):
        me = build.NotionObject()
        me.set('type', 'template_mention')
        me.nest('template_mention', 'type', 'template_mention_user')
        me.nest('template_mention', 'template_mention_user', 'me')
        return cls(_mention_object=me, annotations=annotations)


class Annotations(build.NotionObject):
    __slots__: typing.Sequence[str] = ()

    def __init__(self,
                 bold: bool | None = None,
                 italic: bool | None = None,
                 strike: bool | None = None,
                 underline: bool | None = None,
                 code: bool | None = None,
                 color: NotionColors | None = None ) -> None:
        super().__init__()

        self.set('bold', bold) if bold else None
        self.set('italic', italic) if italic else None
        self.set('strike', strike) if strike else None
        self.set('underline', underline) if underline else None
        self.set('color', color) if color else None
        self.set('color', NotionColors.default) if not color else None
        self.set('code', code) if code else None
        
        if not any([[bold, italic, strike, underline, code, color]]):
            pass # annotations must be defined or non-existent, or Notion will return error
