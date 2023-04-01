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

from functools import cached_property
from types import ModuleType
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    MutableMapping,
    Optional,
    Sequence,
    Union,
    cast,
)

try:
    import orjson

    default_json: ModuleType = orjson
except ModuleNotFoundError:
    import json

    default_json: ModuleType = json

from notion.api.blockmixin import _TokenBlockMixin
from notion.api.client import _NLOG
from notion.api.notionblock import Block
from notion.exceptions.errors import NotionInvalidRequest, NotionObjectNotFound
from notion.properties import *

if TYPE_CHECKING:
    from notion.api.notionpage import Page

__all__: Sequence[str] = ["Database"]


class Database(_TokenBlockMixin):
    """
    Database objects describe the property schema of a database in Notion.
    Pages are the items (or children) in a database. The API treats database rows as pages.

    All databases require one, and only one, title property.
    The API throws errors if you send a request to Create a database without a title property,
    or if you attempt to Update a database to add or remove a title property.

    ### Title database property vs. database title
    A title database property is a type of column in a database.
    A database title defines the title of the database and is found on the database object.
    Every database requires both a database title and a title database property.

    NOTE: Adding a new column with the same name as an existing column will replace the existing column
    with the new column type. If the column of the same name is updated again, but back to the original
    column type - the previous settings (number format, formula expression, etc..) will reapply.

    ---
    :param id: (required) `database_id` of object in Notion.
    :param token: (required) Bearer token provided when you create an integration.\
                   set as `NOTION_TOKEN` in .env or set variable here.\
                   see https://developers.notion.com/reference/authentication.
    :param notion_version: (optional) API version. see https://developers.notion.com/reference/versioning

    ---
    :raises: `notion.exceptions.errors.NotionInvalidRequest` if using an id that does not\
        reference a database in Notion.

    https://developers.notion.com/reference/database
    """

    def __new__(
        cls,
        id: str,
        /,
        token: Optional[str] = None,
        notion_version: Optional[str] = None,
    ) -> Database:
        target_block = Block(id, token=token, notion_version=notion_version)
        if target_block.type != "child_database":
            raise NotionInvalidRequest(
                f"{target_block.__repr__()} does not reference a Database."
            )
        return super().__new__(cls)

    def __init__(
        self,
        id: str,
        /,
        *,
        token: Optional[str] = None,
        notion_version: Optional[str] = None,
    ) -> None:
        super().__init__(id, token=token, notion_version=notion_version)
        if token:
            self.token = token

        self.notion_version: Optional[str] = notion_version
        self.logger = _NLOG.getChild(f"{self.__repr__()}")

    @classmethod
    def create(
        cls, parent_instance: Page, database_title: str, name_column: Optional[str] = None
    ) -> Database:
        """
        Creates a non-inline database in the specified parent page, with the specified properties schema.
        Currently, Databases cannot be created to the parent workspace.


        ---
        :param parent_instance: (required) an instance of `notion.api.notionpage.Page`.
        :param database_title: (required) title of new database.
        :param name_column: (required) name for main column for page names. Defaults to "Name".

        :raises: `NotionObjectNotFound` if trying to create a database directly inside another database.

        https://developers.notion.com/reference/create-a-database
        """
        payload = build_payload(
            Parent.page(parent_instance.id),
            TitlePropertyValue([RichText(database_title)]),
            Properties(TitlePropertyObject(name_column if name_column else "Name")),
        )

        new_db = cls._post(parent_instance, cls._database_endpoint(), payload=payload)

        cls_ = cls(new_db["id"])
        cls_.logger.info(
            f"Database created in {parent_instance.__repr__()}. Url: {new_db['url']}"
        )
        return cls_

    def __getitem__(self, property_name: str) -> MutableMapping[str, Any]:
        try:
            return cast(MutableMapping[str, Any], self._property_schema[property_name])
        except KeyError:
            raise NotionObjectNotFound(
                f"{property_name} not found in page property values."
            )

    @cached_property
    def retrieve(self) -> MutableMapping[str, Any]:
        """https://developers.notion.com/reference/retrieve-a-database"""
        return self._get(self._database_endpoint(self.id))

    @cached_property
    def _property_schema(self) -> MutableMapping[str, Any]:
        return cast(MutableMapping[str, Any], self.retrieve["properties"])

    @property
    def title(self) -> str:
        try:
            return str(self.retrieve["title"][0]["text"]["content"])
        except IndexError:
            return ""  # title is empty.

    @title.setter
    def title(self, __new_title: str) -> None:
        self._update(payload=TitlePropertyValue([RichText(__new_title)]))

    @property
    def inline(self) -> bool:
        """
        Has the value true if the database appears in the page as an inline block.
        Otherwise has the value false if the database appears as a child page.

        returns the current inline status.
        """
        return cast(bool, (self.retrieve["is_inline"]))

    @inline.setter
    def inline(self, __inline: bool) -> None:
        self._patch(
            self._database_endpoint(self.id),
            payload=default_json.dumps({"is_inline": __inline}),
        )

    @property
    def url(self) -> str:
        return str(self.retrieve["url"])

    @property
    def icon(self) -> MutableMapping[str, Any]:
        return cast(MutableMapping[str, Any], self.retrieve["icon"])

    @property
    def delete_self(self) -> None:
        if self.is_archived:
            self.logger.info("delete_self did nothing. Database is already archived.")
            return None

        self._delete(self._block_endpoint(self.id))
        self.logger.info("Deleted self.")

    @property
    def restore_self(self) -> None:
        if not self.is_archived:
            self.logger.info("restore_self did nothing. Database is not archived.")
            return None

        self._patch(self._database_endpoint(self.id), payload=(b'{"archived": false}'))
        self.logger.info("Restored self.")

    def _update(
        self,
        payload: Union[
            MutableMapping[str, Any], Union[Iterable[bytes], bytes, bytearray]
        ],
    ) -> MutableMapping[str, Any]:
        """
        Updates an existing database as specified by the parameters.
        Used internally but optionally can update custom payloads.

        ---
        :param payload: (required) json payload for updated properties parameters.

        https://developers.notion.com/reference/update-a-database
        """
        return self._patch(self._database_endpoint(self.id), payload=payload)

    def delete_property(self, name_or_id: str) -> None:
        """
        :param name_or_id: (required) name or id of property described in database schema

        https://developers.notion.com/reference/update-property-schema-object#removing-a-property
        """
        self._update(payload={"properties": {name_or_id: None}})
        self.logger.info(f"Deleted property `{name_or_id}`")

    def rename_property(self, old_name: str, new_name: str) -> None:
        """
        https://developers.notion.com/reference/update-property-schema-object#renaming-a-property
        """
        self._update(
            payload=default_json.dumps({"properties": {old_name: {"name": new_name}}})
        )
        self.logger.info(f"Renamed property `{old_name}` to `{new_name}`")

    def query(
        self,
        *,
        payload: Optional[
            Union[MutableMapping[str, Any], Union[Iterable[bytes], bytes, bytearray]]
        ] = None,
        filter_property_values: Optional[list[str]] = None,
    ) -> MutableMapping[str, Any]:
        """
        Gets a list of Pages contained in the database,
        filtered/ordered to the filter conditions/sort criteria provided in request.
        The response may contain fewer than page_size of results.
        Responses from paginated endpoints contain a `next_cursor` property,
        which can be used in a query payload to continue the list.
        page_size Default: 100 page_size Maximum: 100.

        ---
        :param payload: (optional) filter/sort objects to apply to query.\
                         filter objects built in `notion.query`
        :param filter_property_values: (optional) list of property names,\
                                        query will only return the selected properties.

        https://developers.notion.com/reference/post-database-query
        """
        query_url = self._database_endpoint(self.id, query=True)

        if filter_property_values:
            query_url = query_url + "?"
            for name in filter_property_values:
                name_id = self._property_schema[name].get("id")
                query_url += "filter_properties=" + name_id + "&"
            return self._post(query_url, payload=payload)

        return self._post(query_url, payload=payload)

    def dual_relation_column(
        self, property_name: str, database_id: str, synced_property_name: str
    ) -> None:
        """
        :param database_id: (required) The database that the relation property refers to.\
                             The corresponding linked page values must belong to the database in order to be valid.
        :param synced_property_name: (required) The name of the corresponding property that is\
                                      updated in the related database when this property is changed.
        """
        self._update(
            Properties(
                RelationPropertyObject.dual(
                    property_name, database_id, synced_property_name
                )
            )
        )

        # NOTE: there is an issue with the current API version and `synced_property_name`,
        # Notion UI will default to `Related to {original database name} ({property name})`,
        # regardless of what name is included in the request.
        # TEMP fix to default synced property name
        synced_database = Database(database_id)
        try:
            synced_database[f"Related to {self.title} ({property_name})"]
            Database(database_id).rename_property(
                f"Related to {self.title} ({property_name})", synced_property_name
            )
        except NotionObjectNotFound:
            pass  # if Notion patches this in between versions

        self.logger.info(
            "%s %s"
            % (
                f"Created/Updated dual_relation property `{property_name}` ",
                f" linked to notion.Database('{database_id}').",
            )
        )

    def single_relation_column(self, property_name: str, database_id: str) -> None:
        self._update(
            Properties(RelationPropertyObject.single(property_name, database_id))
        )
        self.logger.info(
            "%s %s"
            % (
                f"Created/Updated dual_relation property `{property_name}` ",
                f" linked to notion.Database('{database_id}').",
            )
        )

    def rollup_column(
        self,
        property_name: str,
        relation_property_name: str,
        rollup_property_name: str,
        function: Union[FunctionFormat, str],
    ) -> None:
        """
        :param property_name: name for the new rollup column
        :param relation_property_name: name of relation column to other database
        :param rollup_property_name: name of column in other database to calculate
        :param function: `notion.properties.options.FunctionFormat` or refer to api reference.
        """
        self._update(
            (
                Properties(
                    RollupPropertyObject(
                        property_name,
                        relation_property_name,
                        rollup_property_name,
                        function,
                    )
                )
            )
        )
        self.logger.info(f"Created/Updated rollup property `{property_name}`.")

    def select_column(self, property_name: str, /, *, options: list[Option]) -> None:
        """
        If `property_name` is a select column that already exists,
        then the available options will be overwritten with the new list passed to this method.

        You can set the color of an option when first creating it,
        but if `property_name` already existsand a color is assigned in `notion.properties.Option`,
        then `notion.exceptions.errors.NotionValidationError` will raise.

        You can pass an empty list to `options` to clear the available options,
        and then readd them with custom colors.
        """
        self._update(Properties(SelectPropertyObject(property_name, options=options)))
        self.logger.info(f"Created/Updated select property `{property_name}`.")

    def multiselect_column(self, property_name: str, /, *, options: list[Option]) -> None:
        """
        If `property_name` is a multi-select column that already exists,
        then the available options will be overwritten with the new list passed to this method.

        You can set the color of an option when first creating it,
        but if `property_name` already exists and a color is assigned in `notion.properties.Option`,
        then `notion.exceptions.errors.NotionValidationError` will raise.

        You can pass an empty list to `options` to clear the available options,
        and then re-add them with custom colors.
        """
        self._update(
            Properties(MultiSelectPropertyObject(property_name, options=options))
        )
        self.logger.info(f"Created/Updated multi-select property `{property_name}`.")

    def number_column(
        self,
        property_name: str,
        /,
        *,
        format: Optional[Union[NumberFormats, str]] = None,
    ) -> None:
        if not format:
            format = NumberFormats.number
        self._update(Properties(NumberPropertyObject(property_name, format)))
        self.logger.info(f"Created/Updated number property `{property_name}`.")

    def checkbox_column(self, property_name: str) -> None:
        self._update(Properties(CheckboxPropertyObject(property_name)))
        self.logger.info(f"Created/Updated checkbox property `{property_name}`.")

    def date_column(self, property_name: str) -> None:
        self._update(Properties(DatePropertyObject(property_name)))
        self.logger.info(f"Created/Updated date property `{property_name}`.")

    def text_column(self, property_name: str) -> None:
        self._update(Properties(RichTextPropertyObject(property_name)))
        self.logger.info(f"Created/Updated text property `{property_name}`.")

    def formula_column(self, property_name: str, /, *, expression: str) -> None:
        self._update(Properties(FormulaPropertyObject(property_name, expression)))
        self.logger.info(f"Created/Updated formula property `{property_name}`.")

    def created_time_column(self, property_name: str) -> None:
        self._update(Properties(CreatedTimePropertyObject(property_name)))
        self.logger.info(f"Created/Updated created_time property `{property_name}`.")

    def created_by_column(self, property_name: str) -> None:
        self._update(Properties(CreatedByPropertyObject(property_name)))
        self.logger.info(f"Created/Updated created_by property `{property_name}`.")

    def last_edited_time_column(self, property_name: str) -> None:
        self._update(Properties(LastEditedTimePropertyObject(property_name)))
        self.logger.info(f"Created/Updated last_edited property `{property_name}`.")

    def last_edited_by_column(self, property_name: str) -> None:
        self._update(Properties(LastEditedByPropertyObject(property_name)))
        self.logger.info(f"Created/Updated last_edited_by property `{property_name}`.")

    def files_column(self, property_name: str) -> None:
        self._update(Properties(FilesPropertyObject(property_name)))
        self.logger.info(f"Created/Updated files property `{property_name}`.")

    def email_column(self, property_name: str) -> None:
        self._update(Properties(EmailPropertyObject(property_name)))
        self.logger.info(f"Created/Updated email property `{property_name}`.")

    def url_column(self, property_name: str) -> None:
        self._update(Properties(URLPropertyObject(property_name)))
        self.logger.info(f"Created/Updated url property `{property_name}`.")

    def phonenumber_column(self, property_name: str) -> None:
        self._update(Properties(PhoneNumberPropertyObject(property_name)))
        self.logger.info(f"Created/Updated phone_number property `{property_name}`.")

    def people_column(self, property_name: str) -> None:
        self._update(Properties(PeoplePropertyObject(property_name)))
        self.logger.info(f"Created/Updated people property `{property_name}`.")

    # NOTE:
    # It is not possible to update a status database property in the current API version.
    # Update these values from the Notion UI, instead.
