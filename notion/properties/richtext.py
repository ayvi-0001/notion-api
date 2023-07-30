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

from __future__ import annotations

from typing import Optional, Sequence

from notion.properties.build import NotionObject
from notion.properties.common import UserObject, _NotionURL
from notion.properties.options import BlockColor

__all__: Sequence[str] = (
    "Annotations",
    "RichText",
    "Equation",
    "Mention",
)


class RichText(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        content: Optional[str] = None,
        /,
        annotations: Optional[Annotations] = None,
        link: Optional[str] = None,
    ) -> None:
        """
        Rich text objects contain the data that Notion uses to display
        formatted text,mentions, and inline equations.
        Arrays of rich text objects within database property objects and page property value objects
        are used to create what a user experiences as a single text value in Notion.

        https://developers.notion.com/reference/rich-text
        """
        super().__init__()
        self.set("type", "text")
        self.nest("text", "content", content)
        self.nest("text", "link", _NotionURL(link)) if link else None
        if annotations and annotations != {}:
            self.set("annotations", annotations)


class Equation(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self, expression: str, /, *, annotations: Optional[Annotations] = None
    ) -> None:
        """https://developers.notion.com/reference/rich-text#equation"""
        super().__init__()
        self.set("type", "equation")
        self.nest("equation", "expression", expression)
        if annotations and annotations != {}:
            self.set("annotations", annotations)


class Mention(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        *,
        type: str,
        mention_type_object: UserObject | NotionObject,
        annotations: Optional[Annotations] = None,
    ) -> None:
        """
        Use Classmethods:
         - `user`
         - `today`
         - `database`
         - `page`
         - `link_preview`
         - `date`

        https://developers.notion.com/reference/rich-text#mention
        """
        super().__init__()
        self.set("type", "mention")
        self.nest("mention", "type", type)
        self.nest("mention", type, mention_type_object)

        if annotations and annotations != {}:
            self.set("annotations", annotations)

    @classmethod
    def user(
        cls, user_object: UserObject, /, *, annotations: Optional[Annotations] = None
    ) -> Mention:
        """
        If your integration doesn't yet have access to the mentioned user,
        then the plain_text that would include a user's name reads as "@Anonymous".
        To update the integration to get access to the user,
        update the integration capabilities on the integration settings page.

        :raises: `notion.exceptions.errors.NotionValidationError` if trying to mention a Bot.

        https://developers.notion.com/reference/rich-text#user-mention-type-object
        """

        return cls(type="user", mention_type_object=user_object, annotations=annotations)

    @classmethod
    def today(cls, *, annotations: Optional[Annotations] = None) -> Mention:
        """https://developers.notion.com/reference/rich-text#template-mention-type-object"""
        template_mention_date = NotionObject()
        template_mention_date.set("type", "template_mention_date")
        template_mention_date.set("template_mention_date", "today")

        return cls(
            type="template_mention",
            mention_type_object=template_mention_date,
            annotations=annotations,
        )

    @classmethod
    def database(
        cls, database_id: str, *, annotations: Optional[Annotations] = None
    ) -> Mention:
        """https://developers.notion.com/reference/rich-text#database-mention-type-object"""
        database_mention = NotionObject()
        database_mention.set("id", database_id)

        return cls(
            type="database", mention_type_object=database_mention, annotations=annotations
        )

    @classmethod
    def page(cls, page_id: str, *, annotations: Optional[Annotations] = None) -> Mention:
        """https://developers.notion.com/reference/rich-text#page-mention-type-object"""
        page_mention = NotionObject()
        page_mention.set("id", page_id)

        return cls(type="page", mention_type_object=page_mention, annotations=annotations)

    @classmethod
    def link_preview(
        cls, url: str, *, annotations: Optional[Annotations] = None
    ) -> Mention:
        """https://developers.notion.com/reference/rich-text#link-preview-mention-type-object"""
        link_preview_mention = NotionObject()
        link_preview_mention.set("url", url)

        return cls(
            type="link_preview",
            mention_type_object=link_preview_mention,
            annotations=annotations,
        )

    @classmethod
    def date(
        cls,
        start: str,
        end: Optional[str] = None,
        *,
        annotations: Optional[Annotations] = None,
    ) -> Mention:
        """https://developers.notion.com/reference/rich-text#date-mention-type-object"""
        date_mention = NotionObject()
        date_mention.set("start", start)
        date_mention.set("end", end) if end else None

        return cls(type="date", mention_type_object=date_mention, annotations=annotations)


class Annotations(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(
        self,
        bold: Optional[bool] = None,
        italic: Optional[bool] = None,
        strikethrough: Optional[bool] = None,
        underline: Optional[bool] = None,
        code: Optional[bool] = None,
        color: Optional[BlockColor | str] = None,
    ) -> None:
        """https://developers.notion.com/reference/rich-text#the-annotation-object"""
        super().__init__()

        self.set("bold", bold) if bold else None
        self.set("italic", italic) if italic else None
        self.set("strikethrough", strikethrough) if strikethrough else None
        self.set("underline", underline) if underline else None
        self.set("code", code) if code else None
        self.set("color", color) if color else None
