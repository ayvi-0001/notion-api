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

from typing import Sequence, Union

from notion.properties.build import NotionObject
from notion.properties.propertyobjects import PropertyObject
from notion.properties.propertyvalues import PagePropertyValue, TitlePropertyValue

__all__: Sequence[str] = ["Properties"]


class Properties(NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, *properties: Union[PropertyObject, PagePropertyValue]) -> None:
        super().__init__()

        for prop in properties:
            if not hasattr(prop, "name"):
                raise AttributeError(
                    (
                        "`notion.properties.propbuild.Properties` ",
                        "is only used for combining named properties. ",
                        "Check to see if `property_name` has been assigned. ",
                    )
                )

            if isinstance(prop, TitlePropertyValue):
                self.nest("properties", prop.name, prop.get("title"))
            else:
                self.nest("properties", prop.name, prop)
