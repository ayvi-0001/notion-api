from __future__ import annotations

from functools import cached_property
from typing import Sequence
from typing import Union
from datetime import datetime
import pytz 

from notion.properties import *
from notion.core.typedefs import *
from notion.core import notion_logger
from notion.core import request_json

from notion.exceptions.errors import NotionInvalidJson
from notion.exceptions.errors import NotionObjectNotFound
from notion.api.notionblock import Block
from notion.api.notiondatabase import Database
from notion.api.blockmixin import _TokenBlockMixin

__all__: Sequence[str] = ["Page"]


class Page(_TokenBlockMixin):
    """ The Page object contains the page property values of a single Notion page.
    
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
    :param token: (required) Bearer token provided when you create an integration. \
        set as `NOTION_TOKEN` in .env or set variable here. \
        see https://developers.notion.com/reference/authentication.
    :param notion_version: (optional) API version \
        see https://developers.notion.com/reference/versioning
    
    ---
    https://developers.notion.com/reference/page
    """
    def __init__(self, id: str, /, *, token: str | None = None, notion_version: str | None = None):
        super().__init__(id, token=token, notion_version=notion_version)

        self.logger = notion_logger.getChild(f"{self.__repr__()}")


    @classmethod 
    def create(cls, parent_instance: Union[Page, Database, Block], /, *, page_title: str) -> Page:
        """ Creates a blank page with properties. 
        Follow with class methods to add values to properties described in parent database schema, 
        or append block children to include content in the page.

        ---
        :param parent_instance: (required) an instance of \
            `notion.api.notionpage.Page` or `notion.api.notiondatabase.Database`.
        :param page_title: (required)
        :param icon_url: (optional) #not yet implemented
        :param cover: (optional) #not yet implemented

        ---
        https://developers.notion.com/reference/post-page """
        
        if parent_instance.type == 'child_database':
            payload = request_json(Parent.database(parent_instance.id), 
                                   Properties(TitlePropertyValue([RichText(page_title)])))
        else:
            payload = request_json(Parent.page(parent_instance.id), 
                                   Properties(TitlePropertyValue([RichText(page_title)])))

        new_page = cls._post(parent_instance, cls._pages_endpoint(), payload=payload)

        cls(new_page['id']).logger.info(f"Page created in `{parent_instance.__repr__()}`")
        cls(new_page['id']).logger.info(f"Url: {new_page['url']}")

        return cls(new_page['id'])

    def __getitem__(self, property_name: str) -> JSONObject:
        try:
            return self.properties[property_name]
        except KeyError:
            raise NotionObjectNotFound(f"{property_name} not found in page property values.")
    
    @cached_property
    def __page__(self) -> JSONObject:
        return self.retrieve(filter_properties=None)
    
    @property
    def url(self) -> JSONObject:
        return self.__page__['url']
    
    @property
    def icon(self) -> JSONObject:
        return self.__page__['icon']
    
    @property
    def cover(self) -> JSONObject:
        return self.__page__['cover']

    @property
    def delete_self(self) -> None:
        Block(self.id).delete_self()
        self.logger.info('Deleted Self.')
    
    @property
    def properties(self) -> JSONObject:
        return self.retrieve()['properties']

    def retrieve(self, *, filter_properties: list[str] | None = None) -> JSONObject:
        """ Retrieves a Page object using the ID specified.

        ---
        :param filter_properties: (optional) A list of page property value IDs associated with the page. \
            Use this param to limit the response to a specific page property value or values. \
            To retrieve multiple properties, specify each page property ID. \
            E.g. ?filter_properties=iAk8&filter_properties=b7dh.
        --- 
        https://developers.notion.com/reference/retrieve-a-page 
        """
        if filter_properties:
            _pages_endpoint_filtered_prop = self._pages_endpoint(self.id) + '?'
            for name in filter_properties:
                name_id = self.properties[name]['id']
                _pages_endpoint_filtered_prop += 'filter_properties=' + name_id + '&'
            return self._get(_pages_endpoint_filtered_prop)

        return self._get(self._pages_endpoint(self.id))

    def _retrieve_property_id(self, property_name: str, /) -> str:
        """ Internal function to retrieve id of a property. 

        :raises: `notion.exceptions.errors.NotionInvalidJson`
        """
        if property_name in self.properties.keys():
            return self.properties[property_name]['id']
        else:
            raise NotionInvalidJson('Property name not found in page parent schema.')

    def retrieve_property_item(self, property_name: str, /, *, 
                               results_only: bool = False,
                               property_item_only: bool = False
                            #    payload: JSONObject | JSONPayload | None = None
                               ) -> JSONObject:
        """ Retrieves a property_item object for a given page_id and property_id. 
        The object returned will either be a value or a paginated list of property item values.
        
        ---
        :param property_name: (required) property name in Notion *case-sensitive \
            this endpoint only works with property_id's, internal function will retrieve this.
        :param results_only: if true, returns the `results` key index[0] for paginated responses. \
            will be either a single dictionary or a list of dictionaries.
        :param property_item_only: if true, returns the `property_item` key.
        :param payload: NOTE: not yet implemented - for future cursor in paginated responses.
        
        ---
        https://developers.notion.com/reference/retrieve-a-page-property 
        """
        property_id = self._retrieve_property_id(property_name)
        property_item = self._get(self._pages_endpoint(
            self.id, properties=True, property_id=property_id))#, payload=payload)
        
        if results_only and 'results' in property_item.keys():
            return property_item.get('results', [])[0]
        if property_item_only:
            return property_item.get('property_item', {})

        return property_item

    def _patch_properties(self, payload: JSONObject | JSONPayload) -> JSONObject:
        """ Updates page property values for the specified page. 
        Properties that are not set via the properties parameter will remain unchanged.

        If the parent is a database, new property values must conform to the parent database's property schema. 
        
        ---
        https://developers.notion.com/reference/patch-page 
        """
        return self._patch(self._pages_endpoint(self.id), payload=payload)

    def retrieve_page_content(self, start_cursor: str | None = None, 
                                    page_size: int | None = None,
                                    results_only: bool = False) -> JSONObject:
        """
        Returns only the first level of children for the specified block. 
        See block objects for more detail on determining if that block has nested children.
        In order to receive a complete representation of a block, you 
        may need to recursively retrieve block children of child blocks 
        
        NOTE: page_size Default: 100 page_size Maximum: 100.
    
        ---
        https://developers.notion.com/reference/get-block-children
        """
        child_blocks = Block(self.id).retrieve_children(
            page_size=page_size, start_cursor=start_cursor)

        if results_only and 'results' in child_blocks.keys():
            return child_blocks.get('results', {})

        return child_blocks

    def _append(self, payload: JSONObject | JSONPayload) -> JSONObject:
        """ 
        Used internally by `notion.api.blocktypefactory.BlockFactory`.

        https://developers.notion.com/reference/patch-block-children """
        return self._patch(self._block_endpoint(self.id, children=True), payload=payload)

    def rename_page(self, new_name: str) -> None:
        self._patch_properties(Properties(TitlePropertyValue([RichText(new_name)])))
        self.logger.info(f'Renamed page to {new_name}')

    def set_checkbox(self, column_name: str, value: bool, /) -> None: 
        """ 
        :param column_name: (required) column name in Notion UI
        :param value: (required) to replace the current bool
        """
        self._patch_properties(Properties(
            CheckboxPropertyValue(column_name, value)))
    
    def set_text(self, column_name: str, new_text: str, /) -> None:
        """ 
        :param column_name: (required) column name in Notion UI
        :param new_text: (required) to replace the current text
        """
        self._patch_properties(Properties(
            RichTextPropertyValue(column_name, [RichText(new_text)])))
    
    def set_number(self, column_name: str, new_number: int, /) -> None:
        """ 
        :param column_name: (required) column name in Notion UI
        :param new_number: (required) to replace the current number
        """
        self._patch_properties(Properties(
            NumberPropertyValue(column_name, new_number)))

    def set_select(self, column_name: str, select_option: str, /) -> None:
        """ 
        :param column_name: (required) column name in Notion UI
        :param select_option: (required) if the option already exists, then it is \
            case sensitive. if the option does not exist, it will be created.
        """
        self._patch_properties(Properties(
            SelectPropertyValue(column_name, Option(select_option))))

    def set_status(self, column_name: str, status_option: str, /) -> None:
        """ 
        :param column_name: (required) column name in Notion UI
        :param status_option: (required) unlike select/multi-select, status option must already exist \
            when using this endpoint. to create a new status option, use the database endpoints.
        """
        self._patch_properties(Properties(
            StatusPropertyValue(column_name, Option(status_option))))

    def set_multiselect(self, column_name: str, multi_select_options: list[str], /) -> None:
        """ 
        :param column_name: (required) column name in Notion UI
        :param multi_select_options: (required) list of strings for each select option. \
            if the option already exists, then it is case sensitive. \
            if the option does not exist, it will be created.
        """
        selected_options: list[Option] = []
        for option in multi_select_options:
            selected_options.append(Option(option))

        self._patch_properties(Properties(
            MultiSelectPropertyValue(column_name, selected_options)))

    def set_date(self, column_name: str, start: datetime, end=None) -> None:
        """ 
        :param column_name: (required) column name in Notion UI
        :param start: (required) A date, with an optional time. If the "date" value is a range, \
            then start represents the start of the range.
        :param end: (optional) A string representing the end of a date range. \
            If the value is null, then the date value is not a range. 
        """
        if isinstance(start, datetime):
            start = start.replace().astimezone(pytz.timezone(self.default_tz))
        if end and isinstance(end, datetime):
            end = end.replace().astimezone(pytz.timezone(self.default_tz))
        
        self._patch_properties(Properties(
            DatePropertyValue(column_name, start=start, end=end)))

    def set_related(self, column_name: str, related_ids: list[str], /) -> None:
        """ 
        :param column_name: (required) column name in Notion UI
        :param related_ids: (required) list of notion page ids to reference
        """
        list_ids: list[NotionUUID] = []
        for id in related_ids:
            list_ids.append(NotionUUID(id))

        self._patch_properties(Properties(RelationPropertyValue(column_name, list_ids)))
    