# MIT License

# Copyright (c) 2023 ayvi#0001

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

"""
Metadata that controls how a database property behaves. 
Each database property object contain the following; 
 - The ID of the property, usually a short string of random letters and symbols.
   Some automatically generated property types have special human-readable IDs. 
   For example, all Title properties have an ID of "title".name, id, and  key corresponding 
 - The name of the property as it appears in Notion.
 - A key corresponding with the value of type. The value is an object containing 
   type-specific configuration that controls the behavior of the property

NOTE: It is not possible to update a status database property in the current version of the Notion API. 
      Update these values from the Notion UI, instead.

https://developers.notion.com/reference/property-object
"""
from typing import Sequence
from typing import Optional
from typing import Union

from notion.core import build
from notion.exceptions import errors
from notion.properties.options import PropertyColors
from notion.properties.options import NotionNumberFormats
from notion.properties.options import NotionFunctionFormats
from notion.core.typedefs import PropertyObject

__all__: Sequence[str] = (
    "RelationPropertyObject",
    "MultiSelectPropertyObject",
    "SelectPropertyObject",
    "NumberPropertyObject",
    "FormulaPropertyObject",
    "CheckboxPropertyObject",
    "PeoplePropertyObject",
    "PhoneNumberPropertyObject",
    "RichTextPropertyObject",
    "CreatedTimePropertyObject",
    "CreatedByPropertyObject",
    "LastEditedTimePropertyObject",
    "LastEditedByPropertyObject",
    "DatePropertyObject",
    "EmailPropertyObject",
    "FilesPropertyObject",
    "TitlePropertyObject",
    "URLPropertyObject",
    "RollupPropertyObject",
    "Option",
)


class TitlePropertyObject(PropertyObject, build.NotionObject):
    """
    A title database property controls the title that appears at the top of a page when a
    database row is opened. The title type object itself is empty; there is no additional configuration.

    NOTE: All databases require one, and only one, title property.
          The API throws errors if you send a request to Create a database without a title property,
          or if you attempt to Update a database to add or remove a title property.

    ---
    ### Title database property vs. database title
    A title database property is a type of column in a database.
    A database title defines the title of the database and is found on the database object.
    Every database requires both a database title and a title database property.

    https://developers.notion.com/reference/property-object#title
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "title")
        self.set("title", {})


class _Dual_Property(build.NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, database_id: str, synced_property_name: str) -> None:
        super().__init__()
        self.set("database_id", database_id)
        self.set("type", "dual_property")
        self.nest("dual_property", "synced_property_name", synced_property_name)


class _Single_Property(build.NotionObject):
    __slots__: Sequence[str] = ()

    def __init__(self, database_id: str, /) -> None:
        super().__init__()
        self.set("database_id", database_id)
        self.set("type", "single_property")
        self.set("single_property", {})


class RelationPropertyObject(PropertyObject, build.NotionObject):
    """
    Use either classmethod: `dual`/`single`
    
    https://developers.notion.com/reference/property-object#relation
    """

    __slots__: Sequence[str] = ("name", "_related_to_")

    def __init__(
        self,
        property_name: str,
        /,
        *,
        database_id: str,
        synced_property_name: Optional[str] = None,
    ) -> None:
        super().__init__(property_name=property_name)
        self._related_to_: _Dual_Property | _Single_Property

        try:
            self.set("type", "relation")
            self.set("relation", self._related_to_)
        except AttributeError:
            raise errors.NotionInvalidJson("Use classmethods.")

    @classmethod
    def dual(cls, property_name: str, database_id: str, synced_property_name: str, /):
        """
        :param database_id: (required) The database that the relation property refers to.
            The corresponding linked page values must belong to the database in order to be valid.
        :param synced_property_name: (required) The name of the corresponding property that is
            updated in the related database when this property is changed.
        """
        cls._related_to_ = _Dual_Property(database_id, synced_property_name)
        return cls(
            property_name,
            database_id=database_id,
            synced_property_name=synced_property_name,
        )

    @classmethod
    def single(cls, property_name: str, database_id: str, /):
        """
        :param database_id: (required) The database that the relation property refers to.
            The corresponding linked page values must belong to the database in order to be valid.
        """
        cls._related_to_ = _Single_Property(database_id)
        return cls(property_name, database_id=database_id)


class Option(build.NotionObject):
    """
    :param name: (required) The name of the option as it appears in the Notion UI.
        Note: Commas (",") are not valid for select values.
    :param color: (required) The color of the option as rendered in the Notion UI.
        Use `notion.properties.PropertyColor` for reference.
    """

    __slots__: Sequence[str] = ()

    def __init__(
        self, option_name: str, color: Optional[Union[PropertyColors, str]] = None, /
    ) -> None:
        super().__init__()
        self.set("name", option_name)
        if not color:
            self.set("color", PropertyColors.default)
        else:
            self.set("color", color)


class MultiSelectPropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#multi-select"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, *, options: list[Option]) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "multi_select")
        self.nest("multi_select", "options", options)


class SelectPropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#select"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /, *, options: list[Option]) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "select")
        self.nest("select", "options", options)


class NumberPropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#number"""

    __slots__: Sequence[str] = ["name"]

    def __init__(
        self,
        property_name: str,
        format: Optional[Union[NotionNumberFormats, str]] = None,
        /,
    ) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "number")
        if not format:
            self.nest("number", "format", NotionNumberFormats.number)
        else:
            self.nest("number", "format", format)


class FormulaPropertyObject(PropertyObject, build.NotionObject):
    """
    :param expression: (required) The formula that is used to compute the values for this property.
        Refer to the Notion help center for information about formula syntax.
    https://developers.notion.com/reference/property-object#formula
    """

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, expression: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "formula")
        self.nest("formula", "expression", expression)


class CheckboxPropertyObject(PropertyObject, build.NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "checkbox")
        self.set("checkbox", {})


class PeoplePropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#people"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "people")
        self.set("people", {})


class PhoneNumberPropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#phone-number"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "phone_number")
        self.set("phone_number", {})


class RichTextPropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#rich-text"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "rich_text")
        self.set("rich_text", {})


class CreatedTimePropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#created-time"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "created_time")
        self.set("created_time", {})


class CreatedByPropertyObject(PropertyObject, build.NotionObject):
    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "created_by")
        self.set("created_by", {})


class LastEditedTimePropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#last-edited-time"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "last_edited_time")
        self.set("last_edited_time", {})


class LastEditedByPropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#last-edited-by"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "last_edited_by")
        self.set("last_edited_by", {})


class DatePropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#date"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "date")
        self.set("date", {})


class EmailPropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#email"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "email")
        self.set("email", {})


class FilesPropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#files"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "files")
        self.set("files", {})


class URLPropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#url"""

    __slots__: Sequence[str] = ["name"]

    def __init__(self, property_name: str, /) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "url")
        self.set("url", {})


class RollupPropertyObject(PropertyObject, build.NotionObject):
    """https://developers.notion.com/reference/property-object#rollup"""

    __slots__: Sequence[str] = ["name"]

    def __init__(
        self,
        property_name: str,
        relation_property_name: str,
        rollup_property_name: str,
        function: Union[NotionFunctionFormats, str],
        /,
    ) -> None:
        super().__init__(property_name=property_name)
        self.set("type", "rollup")
        self.nest("rollup", "relation_property_name", relation_property_name)
        self.nest("rollup", "rollup_property_name", rollup_property_name)
        self.nest("rollup", "function", function)
