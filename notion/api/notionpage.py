from __future__ import annotations

from typing import Sequence
from typing import Union

from notion.core import *
from notion.exceptions import *
from notion.properties import *
from notion.core.typedefs import *

from notion.core import page_logger
from notion.api.notionblock import Block
from notion.api.notiondatabase import Database
from notion.api.base_object import _BaseNotionBlock

__all__: Sequence[str] = ["Page"]


class Page(_BaseNotionBlock):
    """The Page object contains the page property values of a single Notion page.
    
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
    def create(cls, 
               parent_instance: Union[Page, Database, Block], 
               payload: JSONObject | JSONPayload | None = None, /, 
               *, page_title: str | None = None, 
               icon_url: str | None = None) -> Page | None:

        if payload is not None:
            url = Page(parent_instance.id)._endpoint('pages', object_id=None)
            new_page = Page(parent_instance.id)._post(url, payload=payload)
            new_page_id = new_page.get('id')
            assert new_page_id is not None
            page_logger.info(f"Created a new page in {parent_instance.__repr__()}")
            page_logger.info(f"New page id: {new_page_id}".replace('-',''))

            return cls(new_page_id)

        elif payload is None and page_title is not None:
            if parent_instance.type == 'child_database':
                _parent = Parent.database(parent_instance.id)
            else:
                _parent = Parent.page(parent_instance.id)

            _payload = request_json(
                _parent, Properties(TitlePropertyValue([RichText(page_title)])))

            url = Page(parent_instance.id)._endpoint('pages', object_id=None)
            new_page = Page(parent_instance.id)._post(url, payload=_payload)
            new_page_id = new_page.get('id')
            assert new_page_id is not None

            page_logger.info(f"Created a new page in {parent_instance.__repr__()}")
            page_logger.info(f"New page id: {new_page_id}".replace('-',''))

            return cls(new_page_id)
        
        else:
            page_logger.warn(f"{cls.__repr__} cannot use create() without either payload or pagetitle.")
            return None

    def retrieve(self, *, payload: JSONObject | JSONPayload | None = None) -> JSONObject:
        """Retrieves a Page object using the ID specified. 
        https://developers.notion.com/reference/retrieve-a-page 
        """
        url = super()._endpoint('pages', object_id=self.id)
        return super()._get(url, payload=payload)

    def property_names(self) -> list[str]:
        """Returns property names by default. Set 'ids' to true to return
        Property ids. Response references schema of the parent database.
        """
        if self.parent_type == 'workspace' or self.parent_type == 'id':
            raise ValueError('Only pages in a database will have property ids')
        else:
            return Database(self.parent_id).property_names #type: ignore

    def retrieve_property_item(self, property_id: str, /, 
                               *, payload: JSONObject | JSONPayload | None = None) -> JSONObject:
        """Retrieves a property_item object for a given page_id and 
        property_id. The object returned will either be a value or 
        a paginated list of property item values.
        To obtain property_id's, use the Retrieve a database endpoint. 
        https://developers.notion.com/reference/retrieve-a-page-property 
        """
        url = super()._endpoint('pages', properties=True, property_id=property_id, object_id=self.id)
        return super()._get(url, payload=payload)

    def patch_properties(self, payload: JSONObject | JSONPayload) -> JSONObject:
        """Updates page property values for the specified page. Properties
        that are not set via the properties parameter will remain unchanged.
        If the parent is a database, the new property values in the properties 
        parameter must conform to the parent database's property schema. 
        https://developers.notion.com/reference/patch-page 
        """
        # LIMITATIONS: Updating rollup property values is not supported.
        url = super()._endpoint('pages', object_id=self.id)
        return super()._patch(url, payload=payload)

    def update_checkbox(self, name: str, value: bool, /):
        """Updates the checkbox page property value defined in the parent database schema.
        """
        checkbox = CheckboxPropertyValue(value, property_name=name)
        _payload = request_json(Properties(checkbox))
        url = super()._endpoint('pages', object_id=self.id)
        return super()._patch(url, payload=_payload)
