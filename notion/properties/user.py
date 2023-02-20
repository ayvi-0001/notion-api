from __future__ import annotations
import typing

from notion.core import build

__all__: typing.Sequence[str] = ["UserObject"]


class UserObject(build.NotionObject):
    """ 
    The User object represents a user in a Notion workspace. Users include full workspace members, and integrations. 
    Guests are not included.
    ---
    :param user: Always "user"
    :param id: (required) Unique identifier for this user. *Always present
    :param type: Type of the user. Possible values are "person" and "bot"
    :param name: (optional) User's name, as displayed in Notion.
    :param avatar_url: (optional) Chosen avatar image.
    ---
    User objects appear in the API in nearly all objects returned by the API, including:
        - Block object under created_by and last_edited_by.
        - Page object under created_by and last_edited_by and in people property items.
        - Database object under created_by and last_edited_by.
        - Rich text object, as user mentions.
        - Property object when the property is a people property.
    
    User objects will always contain object and id keys. 
    The remaining properties may appear if the user is being rendered in a rich text or 
    page property context, and the bot has the correct capabilities to access those properties. 
    ---
    All parameters are display-only and cannot be updated in Notion.
    Parameters marked with * are always present in object.
    ---
    https://developers.notion.com/reference/user
    """
    __slots__: typing.Sequence[str] = ('_user', '_person', '_person_email', )

    def __init__(self, id: str, /, *, name: str | None = None, avatar_url: str | None = None, 
                 person_email: str | None = None, type: str) -> None:
        super().__init__()
        self.set('type', 'user')

        if type == 'person':
            self.nest('user', 'object', 'person')
            self.nest('user', 'id', id)
            self.nest('user', 'name', name) if name else None
            self.nest('user', 'person', {'email':person_email}) if person_email else None
            self.nest('user', 'avatar_url', avatar_url) if avatar_url else None

    @classmethod
    def person(cls, id: str, /, *, name: str | None = None, person_email: str | None = None, 
               avatar_url: str | None = None, type: str='person') -> UserObject:
        return cls(id, name=name, person_email=person_email, type=type)

    # @classmethod #TODO
    # def bot(...)
