from typing import Sequence
from typing import Union

from notion.core import build
from notion.core.typedefs import PropertyObject
from notion.core.typedefs import PagePropertyValue
from notion.properties.pagepropertyvalues import TitlePropertyValue

__all__: Sequence[str] = ["Properties"]

__property_error__ = """
`notion.properties.propbuild.Properties` is only used for combining named properties.
Check to see if `property_name` has been assigned."""


class Properties(build.NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, *properties: Union[PropertyObject, PagePropertyValue]) -> None:
        super().__init__()

        for prop in properties:
            if not hasattr(prop, "name"):
                raise AttributeError(__property_error__)

            if isinstance(prop, TitlePropertyValue):
                self.nest("properties", prop.name, prop["title"])
            else:
                self.nest("properties", prop.name, prop)
