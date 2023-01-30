import typing

from notion.core import build

__all__: typing.Sequence[str] = (
    "Parent",
    "NotionUUID",
    "NotionURL",
    "Cursor",
    )


class Parent(build.NotionObject):
    def __init__(self, id: str, /, *, type: str) -> None:
        super().__init__()

        self._parent = build.NotionObject()
        self._parent.set('type', type)
        self._parent.set(type, id)
        self.set('parent', self._parent)

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
    def __init__(self, url: str | None = None, /) -> None:
        super().__init__()
        self.set('url', url)


class NotionUUID(build.NotionObject):
    def __init__(self, id: str, /) -> None:
        super().__init__()
        self.set('id', id)


class Cursor(build.NotionObject):
    def __init__(self, id: str, /) -> None:
        super().__init__()
        self.set('next_cursor', id)

#TODO Description
#TODO Move Caption here
