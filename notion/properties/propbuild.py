import typing

from notion.core import build
from notion.core.typedefs import PropertyObject
from notion.core.typedefs import PagePropertyValue
from notion.properties.pagepropertyvalues import TitlePropertyValue

__all__: typing.Sequence[str] = ["Properties"]


class Properties(build.NotionObject):
    __slots__: typing.Sequence[str] = ('_combined_properties')
    
    def __init__(self, *properties: PropertyObject | PagePropertyValue) -> None:
        super().__init__()

        self._combined_properties = build.NotionObject()

        for prop in properties:
            if hasattr(prop, 'name') is False:
                raise AttributeError("""
                `notion.properties.Properties` is only used for combining named properties.
                Check to see if `property_name` has been assigned.""")

            else:
                if isinstance(prop, TitlePropertyValue):
                    self._combined_properties.set(prop.name, prop['title'])
                else:      
                    self._combined_properties.set(prop.name, prop) # type: ignore[union-attr]

        self.set('properties', self._combined_properties)
