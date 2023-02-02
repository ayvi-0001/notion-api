from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Sequence
from functools import cached_property

from notion.core import *
from notion.exceptions import *
from notion.properties import *
from notion.core.typedefs import *
from notion.api.base_object import _BaseNotionBlock

if TYPE_CHECKING:
    from notion.api.notionpage import Page

__all__: Sequence[str] = ['Database']


class Database(_BaseNotionBlock):
    """ Database objects describe the property schema of a database in Notion. 
    Pages are the items (or children) in a database. 
    
    Page property values must conform to the property objects laid out in the 
    parent database object.
    ---
    https://developers.notion.com/reference/database
    """ 
    def __new__(cls, id: str, /, *, token: str | None = None, notion_version: str | None = None):
        if _BaseNotionBlock(id).type != 'child_database':
            raise ValueError(
                f"{cls.__name__}('{id}') does not reference a Database") 
        else: 
            return super().__new__(cls)

    @classmethod
    def create(cls, parent_instance: Page, /, *, page_title: str, name_column: str) -> Database:
        """ 
        Creates a non-inline database in the specified parent page, 
        with the specified properties schema.
        Currently, Databases cannot be created to the parent workspace.
        ---
        (required)
        :param page_title: title of new database.
        :param name_column: name of the `Pages` column. The API treats database rows as pages.
        ---
        https://developers.notion.com/reference/post-page 
        """ 
        if parent_instance.type == 'child_database':
            raise NotionInvalidRequest('Cannot create a database in a database')
        
        payload = request_json(Parent.page(parent_instance.id), 
                               TitlePropertyValue([RichText(page_title)]),
                               Properties(TitlePropertyObject(name_column)))
        
        new_db = cls._post(parent_instance, cls._database_endpoint(), payload=payload)
        database_logger.info(f"Database created in `{parent_instance.__repr__()}`")
        database_logger.info(f"New database id: {new_db['id']} url: {new_db['url']}")

        return cls(new_db['id'])
    
    def toggl_inline(self, inline: bool) -> None:
        """ Has the value true if the database appears in the page as an inline block. 
        Otherwise has the value false if the database appears as a child page. 
        """
        self._patch(self._database_endpoint(self.id), payload={'is_inline':inline})

    @cached_property
    def retrieve(self) -> JSONObject:
        """ Retrieves a Database object using the ID specified. 
        https://developers.notion.com/reference/retrieve-a-database
        """ 
        return self._get(self._database_endpoint(self.id))

    @cached_property
    def property_schema(self) -> JSONObject:
        return self.retrieve['properties']

    def update(self, payload: JSONObject | JSONPayload) -> JSONObject:
        """ Updates an existing database as specified by the parameters. 
        https://developers.notion.com/reference/update-a-database 
        """ 
        return self._patch(self._database_endpoint(self.id), payload=payload)

    def delete_property(self, name_or_id: str) -> None:
        """ Delete a property by either the property name or id. 
        This can be found in the schema with Database.retrieve() 
        """ 
        self.update(payload={'properties':{name_or_id:None}})
    
    def rename_property(self, old_name: str, new_name: str) -> None:
        """ Rename a property by either the property name or id. 
        This can be found in the schema with Database.retrieve() 
        """ 
        self.update(payload={'properties':{old_name:{'name':new_name}}})
    
    def query(self, /, *, payload: JSONObject | JSONPayload | None = None,
              filter_property_values: list[str] | None = None) -> JSONObject:
        """ Gets a list of Pages contained in the database, filtered/ordered 
        to the filter conditions/sort criteria provided in request. 
        The response may contain fewer than page_size of results. 
        Responses from paginated endpoints contain a `next_cursor` property, 
        which can be used in a query payload to continue the list.
        ---
        (optional)
        :param payload: filter/sort objects to apply to query.
        :param filter_property_values: list of property names, query will only
                                       return the selected properties.
        ---
        NOTE: page_size Default: 100 page_size Maximum: 100.
        https://developers.notion.com/reference/update-a-database 
        """ 
        query_url = self._database_endpoint(self.id, query=True)
        if filter_property_values:
            query_url = query_url + '?'
            for name in filter_property_values:
                name_id = self.property_schema[name]['id']
                query_url += 'filter_properties=' + name_id + '&'        
            return self._post(query_url, payload=payload)
        else:
            return self._post(query_url, payload=payload)

    # adding a column with a name that already exists will replace the old column
    def add_checkbox_column(self, property_name) -> None:
        self.update(request_json(Properties(
            CheckboxPropertyObject(property_name=property_name))))

    def add_date_column(self, property_name) -> None:
        self.update(request_json(Properties(
            DatePropertyObject(property_name=property_name))))

    def add_text_column(self, property_name) -> None:
        self.update(request_json(Properties(
            RichTextPropertyObject(property_name=property_name))))
    
    def add_number_column(self, property_name, /, 
                          *, format: NumberEnum | str = NumberEnum.number) -> None:
        self.update(request_json(Properties(
            NumberPropertyObject(format, property_name=property_name))))

    def add_formula_column(self, property_name, /, *, expression) -> None:
        self.update(request_json(Properties(
            FormulaPropertyObject(expression, property_name=property_name))))

    # TODO: the rest..
    # def ...
