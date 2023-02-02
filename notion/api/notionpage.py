from __future__ import annotations

from typing import Sequence
from typing import Union
from datetime import datetime
import pytz #type: ignore[import]

from notion.core import *
from notion.exceptions import *
from notion.properties import *
from notion.core.typedefs import *

from notion.api.notionblock import Block
from notion.api.notiondatabase import Database
from notion.api.base_object import _BaseNotionBlock

__all__: Sequence[str] = ["Page"]


class Page(_BaseNotionBlock):
    """ The Page object contains the page property values of a single Notion page.
    
    All pages have a Parent. If the parent is a database, 
    the property values conform to the schema laid out database's properties.
    Otherwise, the only property value is the title.

    Page content is available as blocks. 
    The content can be read using retrieve block children and 
    appended using append block children. 
    
    Current version of the api does not allow pages to be created
    to the parent `workspace`
    ---
    https://developers.notion.com/reference/page
    """
    def __init__(self, id: str, /, *, token: str | None = None, notion_version: str | None = None):
        super().__init__(id, token=token, notion_version=notion_version)


    @classmethod 
    def create(cls, parent_instance: Union[Page, Database, Block], /, *, page_title: str) -> Page:
        """ Creates a blank page with properties. 
        Follow with class methods to add any properties described in parent database schema, 
        or append block children to include content in the page.
        ---
        (required)
        :param page_title:
        ---
        (optional)
        :param icon_url: #not yet implemented
        :param cover: #not yet implemented
        ---
        https://developers.notion.com/reference/post-page """
        
        if parent_instance.type == 'child_database':
            payload = request_json(Parent.database(parent_instance.id), 
                                   Properties(TitlePropertyValue([RichText(page_title)])))
        else:
            payload = request_json(Parent.page(parent_instance.id), 
                                   Properties(TitlePropertyValue([RichText(page_title)])))

        new_page = cls._post(parent_instance, cls._pages_endpoint(), payload=payload)
        page_logger.info(f"Page created in `{parent_instance.__repr__()}`")
        page_logger.info(f"New page id: {new_page['id']} url: {new_page['url']}")

        return cls(new_page['id'])

    def retrieve(self, *, filter_properties: list[str] | None = None) -> JSONObject:
        """ Retrieves a Page object using the ID specified.

        (optional)
        :param filter_properties: A list of page property value IDs associated with the page. 
                                  Use this param to limit the response to a specific page property value or values. 
                                  To retrieve multiple properties, specify each page property ID. 
                                  For example: ?filter_properties=iAk8&filter_properties=b7dh.
        --- 
        https://developers.notion.com/reference/retrieve-a-page 
        """
        if filter_properties:
            _pages_endpoint_filtered_prop = self._pages_endpoint(self.id) + '?'
            for name in filter_properties:
                name_id = self.properties[name]['id']
                _pages_endpoint_filtered_prop += 'filter_properties=' + name_id + '&'
            return self._get(_pages_endpoint_filtered_prop)
        else:
            return self._get(self._pages_endpoint(self.id))

    @property
    def properties(self) -> JSONObject:
        return self.retrieve()['properties']

    def _retrieve_property_id(self, property_name: str, /) -> str:
        """ Internal function to retrieve id of a property. """
        properties = self.properties
        if property_name in properties.keys():
            return properties[property_name]['id']
        else:
            raise NotionInvalidJson('Property name not found in page parent schema.')

    def retrieve_property_item(self, property_name: str, /, 
                               *, payload: JSONObject | JSONPayload | None = None) -> JSONObject:
        """ Retrieves a property_item object for a given page_id and property_id. 
        The object returned will either be a value or a paginated list of property item values.
        ---
        (required)
        :param property_name: property name in Notion *case-sensitive
        ---
        https://developers.notion.com/reference/retrieve-a-page-property 
        """
        property_id = self._retrieve_property_id(property_name)
        return self._get(self._pages_endpoint(
            self.id, properties=True, property_id=property_id), payload=payload)

    def patch_properties(self, payload: JSONObject | JSONPayload) -> JSONObject:
        """ Updates page property values for the specified page. 
        Properties that are not set via the properties parameter will remain unchanged.
        If the parent is a database, new property values must conform to the parent database's property schema. 
        ---
        LIMITATIONS: Updating rollup property values is not supported.
        
        ---
        https://developers.notion.com/reference/patch-page 
        """
        return self._patch(self._pages_endpoint(self.id), payload=payload)

    def append_to_page(self, payload: JSONObject | JSONPayload) -> JSONObject:
        return self._patch(self._block_endpoint(self.id, children=True), payload=payload)

    def set_checkbox(self, column_name: str, value: bool, /) -> JSONObject: 
        payload = request_json(Properties(
            CheckboxPropertyValue(value, property_name=column_name)))
        return self._patch(self._pages_endpoint(self.id), payload=payload)
    
    def set_text(self, column_name: str, new_text: str, /) -> JSONObject: 
        payload = request_json(Properties(
            RichTextPropertyValue([RichText(new_text)], property_name=column_name)))
        return self._patch(self._pages_endpoint(self.id), payload=payload)
    
    def set_number(self, column_name: str, new_number: int, /) -> JSONObject: 
        payload = request_json(Properties(
            NumberPropertyValue(new_number, property_name=column_name)))
        return self._patch(self._pages_endpoint(self.id), payload=payload)

    # select/status is case sensitive if option already exists
    def set_select(self, column_name: str, select_option: str, /) -> JSONObject: 
        payload = request_json(Properties(
            SelectPropertyValue(Option(select_option), property_name=column_name)))
        return self._patch(self._pages_endpoint(self.id), payload=payload)

    def set_status(self, column_name: str, status_option: str, /) -> JSONObject: 
        # status doesn't create new option like selects
        payload = request_json(Properties(
            StatusPropertyValue(Option(status_option), property_name=column_name)))
        return self._patch(self._pages_endpoint(self.id), payload=payload)

    def set_multiselect(self, column_name: str, multi_select_options: list[str], /) -> JSONObject: 
        selected_options: list = []
        for option in multi_select_options:
            selected_options.append(Option(option))

        payload = request_json(Properties(
            MultiSelectPropertyValue(selected_options, property_name=column_name)))
        return self._patch(self._pages_endpoint(self.id), payload=payload)

    def set_date(self, column_name: str, start: datetime, end=None) -> JSONObject: 
        if isinstance(start, datetime):
            start = start.replace().astimezone(pytz.timezone(self.default_tz))
        if end and isinstance(end, datetime):
            end = end.replace().astimezone(pytz.timezone(self.default_tz))
        
        payload = request_json(Properties(
            DatePropertyValue(start=start, end=end, property_name=column_name)))
        return self._patch(self._pages_endpoint(self.id), payload=payload)

    def set_related(self, column_name: str, related_ids: list[str], /) -> JSONObject: 
        selected_options: list = []
        for id in related_ids:
            selected_options.append(NotionUUID(id))

        payload = request_json(Properties(
            RelationPropertyValue(selected_options, property_name=column_name)))
        return self._patch(self._pages_endpoint(self.id), payload=payload)
