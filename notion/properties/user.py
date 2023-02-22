from __future__ import annotations
from typing import Sequence
from typing import Optional

from notion.core import build

__all__: Sequence[str] = ["UserObject"]


class UserObject(build.NotionObject):
    """ 
    The User object represents a user in a Notion workspace. Users include full workspace members, and integrations. 
    Guests are not included.

    ---
    :param id: (required) Unique identifier for this user. *Always present
    :param name: (optional) User's name, as displayed in Notion.
    :param avatar_url: (optional)
    :param email: (optional)
    
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
    
    ---
    https://developers.notion.com/reference/user
    """
    __slots__: Sequence[str] = ()

    def __init__(self, id: str, name: Optional[str] = None, avatar_url: Optional[str] = None, 
                 email: Optional[str] = None) -> None:
        super().__init__()
        self.set('object', 'user')
        self.set('id', id)
        self.set('name', name) if name else None
        self.set('avatar_url', avatar_url) if avatar_url else None
        self.set('type', 'person')
        if email:
            self.nest('person', 'email', email)
        else:
            self.set('person', {}) # must be at least an empty object.
        
