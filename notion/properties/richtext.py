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
from notion.properties.options import ColorEnum
from notion.properties.common import NotionURL
from notion.properties.common import NotionUUID

__all__: typing.Sequence[str] = (
    "Annotations",
    "RichText",
    "Equation",
    "Mention",
    )


class RichText(build.NotionObject):
    __slots__: typing.Sequence[str] = ('_text')

    def __init__(self, content: str, /, *, link: str | None = None, 
                 annotations: Annotations | None = None) -> None:
        super().__init__()

        self._text = build.NotionObject()
        self._text.set('content', content)
        self._text.set('link', NotionURL(link)) if link else None
        self.set('type', 'text')
        self.set('text', self._text)
        if annotations is not None and annotations != {}:
            self.set('annotations', annotations)


class Equation(build.NotionObject):
    __slots__: typing.Sequence[str] = ('_equation')

    def __init__(self, expression: str, /, *, annotations: Annotations | None = None) -> None:
        super().__init__()

        self._equation = build.NotionObject()
        self._equation.set('expression', expression)
        self.set('type', 'equation')
        self.set('equation', self._equation)
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
        return cls(_mention_object=user_object, annotations=annotations)

    @classmethod
    def link(cls, url, /, *, annotations: Annotations | None = None):
        link_preview = build.NotionObject()
        _url = build.NotionObject()
        _url.set('url', url)
        link_preview.set('type', 'link_preview')
        link_preview.set('link_preview', _url)
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
        template_mention_date = build.NotionObject()
        template_mention_date.set('type', 'template_mention_date')
        template_mention_date.set('template_mention_date', 'today')
        today.set('type', 'template_mention')
        today.set('template_mention', template_mention_date)
        return cls(_mention_object=today, annotations=annotations)

    @classmethod
    def now(cls, /, *, annotations: Annotations | None = None):
        now = build.NotionObject()
        template_mention_date = build.NotionObject()
        template_mention_date.set('type', 'template_mention_date')
        template_mention_date.set('template_mention_date', 'now')
        now.set('type', 'template_mention')
        now.set('template_mention', template_mention_date)
        return cls(_mention_object=now, annotations=annotations)

    @classmethod
    def me(cls, /, *, annotations: Annotations | None = None):
        me = build.NotionObject()
        template_mention_user = build.NotionObject()
        template_mention_user.set('type', 'template_mention_user')
        template_mention_user.set('template_mention_user', 'me')
        me.set('type', 'template_mention')
        me.set('template_mention', template_mention_user)
        return cls(_mention_object=me, annotations=annotations)


class Annotations(build.NotionObject):
    __slots__: typing.Sequence[str] = ()

    def __init__(self,
                 bold: bool | None = False,
                 italic: bool | None = False,
                 strike: bool | None = False,
                 underline: bool | None = False,
                 code: bool | None = False,
                 color: ColorEnum | None = None ) -> None:
        super().__init__()

        if any([bold, italic, strike, underline, code, color]):
            self.set('bold', bold)
            self.set('italic', italic)
            self.set('strike', strike)
            self.set('underline', underline)
            self.set('code', code)
            self.set('color', color)
        else:
            pass
