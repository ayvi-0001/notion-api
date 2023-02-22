from typing import Sequence
from typing import Optional

from notion.core import build

__all__: Sequence[str] = (
    "Parent",
    "NotionUUID",
    "NotionURL",
)


class Parent(build.NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, id: str, /, *, type: str) -> None:
        super().__init__()
        self.nest('parent', 'type', type)
        self.nest('parent', type, id)

    @classmethod
    def page(cls, id: str, /, *, type: str='page_id'):
        return cls(id, type=type)

    @classmethod
    def database(cls, id: str, /, *, type: str='database_id'):
        return cls(id, type=type)

    @classmethod
    def block(cls, id: str, /, *, type: str='block_id'):
        return cls(id, type=type)


class NotionURL(build.NotionObject):
    __slots__: Sequence[str] = ()
    
    def __init__(self, url: Optional[str] = None, /) -> None:
        super().__init__()
        self.set('url', url)


class NotionUUID(build.NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, id: str) -> None:
        super().__init__()
        self.set('id', id)

#TODO 
    # Database Description
    # Cursor
