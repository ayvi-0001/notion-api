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

from datetime import datetime
from functools import cached_property, reduce
from operator import getitem
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    MutableMapping,
    Optional,
    Sequence,
    Union,
)

from jsonpath_ng.ext import parse  # type: ignore[import]

from notion.api.blockmixin import _TokenBlockMixin
from notion.api.client import _NLOG
from notion.api.notionblock import Block
from notion.api.notiondatabase import Database
from notion.exceptions.errors import NotionInvalidJson, NotionObjectNotFound
from notion.properties import *
from notion.properties.build import build_payload

if TYPE_CHECKING:
    from datetime import timedelta

__all__: Sequence[str] = ["Page"]


class Page(_TokenBlockMixin):
    """
    The Page object contains the page property values of a single Notion page.
    All pages have a Parent. If the parent is a database,
    the property values conform to the schema laid out database's properties.
    Otherwise, the only property value is the title.

    Page content is available as blocks.
    Content can be read using retrieve block children and appended using append block children.

    NOTE: The current version of the Notion api does not allow pages to be created
    to the parent `workspace`. This is why it's necessary to pass a parent instance
    `notion.api.notionpage.Page` or `notion.api.notiondatabase.Database` to the `create`
    class methods, to provide a valid parent id.

    ---
    :param id: (required) `page_id` of object in Notion.
    :param token: (required) Bearer token provided when you create an integration.
        set as `NOTION_TOKEN` in .env or set variable here.
        see https://developers.notion.com/reference/authentication.
    :param notion_version: (optional) API version
        see https://developers.notion.com/reference/versioning

    https://developers.notion.com/reference/page
    """

    def __init__(
        self,
        id: str,
        /,
        *,
        token: Optional[str] = None,
        notion_version: Optional[str] = None,
    ) -> None:
        super().__init__(id, token=token, notion_version=notion_version)

        self.logger = _NLOG.getChild(f"{self.__repr__()}")

    @classmethod
    def create(
        cls, parent_instance: Union[Page, Database, Block], /, *, page_title: str
    ) -> Page:
        """
        Creates a blank page with properties.
        Follow with class methods to add values to properties described in parent database schema,
        or append block children to include content in the page.

        ---
        :param parent_instance: (required) an instance of
            `notion.api.notionpage.Page` or `notion.api.notiondatabase.Database`.
        :param page_title: (required)
        :param icon_url: (optional) #not yet implemented
        :param cover: (optional) #not yet implemented

        https://developers.notion.com/reference/post-page
        """
        if parent_instance.type == "child_database":
            payload = build_payload(
                Parent.database(parent_instance.id),
                Properties(TitlePropertyValue([RichText(page_title)])),
            )
        else:
            payload = build_payload(
                Parent.page(parent_instance.id),
                Properties(TitlePropertyValue([RichText(page_title)])),
            )

        new_page = cls._post(parent_instance, cls._pages_endpoint(), payload=payload)

        cls_ = cls(new_page["id"])
        cls_.logger.info(f"Page created in {parent_instance.__repr__()}")
        cls_.logger.info(f"Url: {new_page['url']}")

        return cls_

    def __getitem__(self, property_name: str) -> MutableMapping[str, Any]:
        try:
            return self.properties[property_name]  # type: ignore[no-any-return]
        except KeyError:
            raise NotionObjectNotFound(
                f"{property_name} not found in page property values."
            )

    @cached_property
    def _retrieve(self) -> MutableMapping[str, Any]:
        return self.retrieve(filter_properties=None)

    @cached_property
    def properties(self) -> MutableMapping[str, Any]:
        return self._retrieve["properties"]  # type: ignore[no-any-return]

    @property
    def title(self) -> str:
        title_keys = ["properties", "title", "title", 0, "text", "content"]
        try:
            return str(reduce(getitem, title_keys, self._retrieve))  # type: ignore[arg-type]
        except IndexError:
            return ""  # page title is empty.

    @title.setter
    def title(self, __new_title: str) -> None:
        self._patch_properties(
            payload=Properties(TitlePropertyValue([RichText(__new_title)]))
        )

    @property
    def url(self) -> MutableMapping[str, Any]:
        return self._retrieve["url"]  # type: ignore[no-any-return]

    @property
    def icon(self) -> MutableMapping[str, Any]:
        return self._retrieve["icon"]  # type: ignore[no-any-return]

    @property
    def cover(self) -> MutableMapping[str, Any]:
        return self._retrieve["cover"]  # type: ignore[no-any-return]

    @property
    def delete_self(self) -> None:
        self._delete(self._block_endpoint(self.id))
        self.logger.info("Deleted self.")

    @property
    def restore_self(self) -> None:
        self._patch(self._pages_endpoint(self.id), payload=(b'{"archived": false}'))
        self.logger.info("Restored self.")

    def retrieve(
        self, *, filter_properties: Optional[list[str]] = None
    ) -> MutableMapping[str, Any]:
        """
        Retrieves a Page object using the ID specified.

        ---
        :param filter_properties: (optional) A list of page property value IDs associated with the page.
            Use this param to limit the response to a specific page property value or values.
            To retrieve multiple properties, specify each page property ID.
            E.g. ?filter_properties=iAk8&filter_properties=b7dh.

        https://developers.notion.com/reference/retrieve-a-page
        """
        if filter_properties:
            _pages_endpoint_filtered_prop = f"{self._pages_endpoint(self.id)}?"
            for name in filter_properties:
                name_id = self.properties[name]["id"]
                _pages_endpoint_filtered_prop += f"filter_properties={name_id}&"
            return self._get(_pages_endpoint_filtered_prop)
        else:
            return self._get(self._pages_endpoint(self.id))

    def _retrieve_property_id(self, property_name: str) -> str:
        """Internal function to retrieve the id of a property.

        :raises: `notion.exceptions.errors.NotionInvalidJson`
        """
        if property_name in self.properties:
            return str(self.properties[property_name]["id"])
        else:
            raise NotionInvalidJson("Property name not found in parent schema.")

    def retrieve_property_item(
        self,
        property_name: str,
    ) -> MutableMapping[str, Any]:
        """
        Retrieves a property_item object for a given page_id and property_id.
        The object returned will either be:
            - a value.
            - a paginated list of property item values.

        ---
        :param property_name: (required) property name in Notion *case-sensitive
            this endpoint only works with property_id's, internal function will retrieve this.
        :param results_only: if true, returns the `results` key index[0] for paginated responses.
            will be either a single dictionary or a list of dictionaries.
        :param property_item_only: if true, returns the `property_item` key.

        https://developers.notion.com/reference/retrieve-a-page-property
        """
        return self._get(
            self._pages_endpoint(
                self.id,
                properties=True,
                property_id=self._retrieve_property_id(property_name),
            )
        )

    def _patch_properties(
        self,
        payload: Union[
            MutableMapping[str, Any], Union[Iterable[bytes], bytes, bytearray]
        ],
    ) -> MutableMapping[str, Any]:
        """
        Updates page property values for the specified page.
        Properties not set via the properties parameter will remain unchanged.
        If the parent is a database,
        new property values must conform to the parent database's property schema.

        https://developers.notion.com/reference/patch-page
        """
        return self._patch(self._pages_endpoint(self.id), payload=payload)

    def retrieve_page_content(
        self,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> MutableMapping[str, Any]:
        """
        Returns only the first level of children for the specified block.
        See block objects for more detail on determining if that block has nested children.
        In order to receive a complete representation of a block, you
        may need to recursively retrieve block children of child blocks.
        page_size Default: 100 page_size Maximum: 100.

        https://developers.notion.com/reference/get-block-children
        """
        return Block(self.id).retrieve_children(
            page_size=page_size, start_cursor=start_cursor
        )

    def _append(
        self,
        payload: Union[
            MutableMapping[str, Any], Union[Iterable[bytes], bytes, bytearray]
        ],
    ) -> MutableMapping[str, Any]:
        """
        Used internally by `notion.api.blocktypefactory.BlockFactory`.

        https://developers.notion.com/reference/patch-block-children
        """
        return self._patch(
            self._block_endpoint(self.id, children=True), payload=payload
        )

    def set_select(self, column_name: str, select_option: str) -> None:
        """
        :param select_option: (required) if the option already exists, then it is
            case sensitive. if the option does not exist, it will be created.
        """
        color = [
            m.value
            for m in parse(
                f"$.select.options[?(@.name=='{select_option}')].color"
            ).find(Database(self.parent_id)[column_name])
        ]

        if color[0]:
            self._patch_properties(
                Properties(
                    SelectPropertyValue(column_name, Option(select_option, color[0]))
                )
            )
        else:
            self._patch_properties(
                Properties(SelectPropertyValue(column_name, Option(select_option)))
            )

    def set_multiselect(
        self, column_name: str, multi_select_options: list[str]
    ) -> None:
        """
        :param multi_select_options: (required) list of strings for each select option.
            if the option already exists, then it is case sensitive.
            if the option does not exist, it will be created.
        """
        selected_options: list[Option] = []

        for option in multi_select_options:
            color = [
                m.value
                for m in parse(
                    f"$.multi_select.options[?(@.name=='{option}')].color"
                ).find(Database(self.parent_id)[column_name])
            ]
            if color[0]:
                selected_options.append(Option(option, color[0]))
            else:
                selected_options.append(Option(option))

        self._patch_properties(
            Properties(MultiSelectPropertyValue(column_name, selected_options))
        )

    def set_status(self, column_name: str, status_option: str) -> None:
        """
        :param status_option: (required) unlike select/multi-select,
            status option must already exist when using this endpoint.
            to create a new status option, use the database endpoints.
        """
        color = [
            m.value
            for m in parse(
                f"$.status.options[?(@.name=='{status_option}')].color"
            ).find(Database(self.parent_id)[column_name])
        ]

        if color[0]:
            self._patch_properties(
                Properties(
                    StatusPropertyValue(column_name, Option(status_option, color[0]))
                )
            )
        else:
            self._patch_properties(
                Properties(StatusPropertyValue(column_name, Option(status_option)))
            )

    def set_date(
        self,
        column_name: str,
        start: Union[str, datetime],
        end: Optional[Union[str, datetime]] = None,
    ) -> None:
        """
        :param start: (required) A date, with an optional time.
            If the "date" value is a range, then start represents the start of the range.
        :param end: (optional) A string representing the end of a date range.
            If the value is null, then the date value is not a range.
        """
        if isinstance(start, datetime):
            start = start.replace().astimezone(self.tz)
        if end and isinstance(end, datetime):
            end = end.replace().astimezone(self.tz)

        self._patch_properties(
            Properties(DatePropertyValue(column_name, start=start, end=end))
        )

    def set_text(self, column_name: str, new_text: Union[str, Any]) -> None:
        """
        :param new_text: (required) to replace the current text
        """
        self._patch_properties(
            Properties(RichTextPropertyValue(column_name, [RichText(new_text)]))
        )

    def set_files(
        self, column_name: str, array_of_files: list[Union[InternalFile, ExternalFile]]
    ) -> None:
        self._patch_properties(
            Properties(FilesPropertyValue(column_name, array_of_files))
        )

    def set_phonenumber(self, column_name: str, phone_number: str) -> None:
        self._patch_properties(
            Properties(PhoneNumberPropertyValue(column_name, phone_number))
        )

    def set_related(self, column_name: str, related_ids: list[str]) -> None:
        """
        :param related_ids: (required) list of notion page ids to reference
        """
        list_ids: list[NotionUUID] = []
        for id in related_ids:
            list_ids.append(NotionUUID(id))

        self._patch_properties(Properties(RelationPropertyValue(column_name, list_ids)))

    def set_checkbox(self, column_name: str, value: bool) -> None:
        """
        :param value: (required) to replace the current bool
        """
        self._patch_properties(Properties(CheckboxPropertyValue(column_name, value)))

    def set_number(self, column_name: str, new_number: Union[float, timedelta]) -> None:
        """
        :param new_number: (required) to replace the current number
        """
        self._patch_properties(Properties(NumberPropertyValue(column_name, new_number)))

    def set_people(self, column_name: str, user_array: list[UserObject]) -> None:
        self._patch_properties(Properties(PeoplePropertyValue(column_name, user_array)))

    def set_email(self, column_name: str, email: str) -> None:
        self._patch_properties(Properties(EmailPropertyValue(column_name, email)))

    def set_url(self, column_name: str, url: str) -> None:
        self._patch_properties(Properties(URLPropertyValue(column_name, url)))
