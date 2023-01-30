from __future__ import annotations

from typing import Sequence
from functools import cached_property

from notion.core import *
from notion.exceptions import *
from notion.properties import *
from notion.core.typedefs import *
from notion.core import database_logger
from notion.api.base_object import _BaseNotionBlock

__all__: Sequence[str] = ['Database']


class Database(_BaseNotionBlock):
    """Database objects describe the property schema of a database in Notion. 
    Pages are the items (or children) in a database. 
    
    Page property values must conform to the property objects laid out in the 
    parent database object.
    ---
    https://developers.notion.com/reference/database
    """
    def __new__(cls, id: str, /, *, token: str | None = None, notion_version: str | None = None):
        _block = _BaseNotionBlock(id)
        if _block.type != 'child_database':
            raise ValueError(
                f"{cls.__name__}('{id}') does not reference a Database") 
        else: 
            return super().__new__(cls)

    @classmethod
    def create(cls, parent_instance: _BaseNotionBlock, /, 
               *, payload: JSONObject | JSONPayload | None = None) -> Database:
        """
        Minimum objects required in payload:
        :parent object, and properities with a title object:

        Creates a non-inline database in the specified parent page, 
        with the specified properties schema.
        Currently, Databases cannot be created to the parent workspace.
        ---
        https://developers.notion.com/reference/post-page 
        """
        if parent_instance.type == 'child_database':
            raise ValueError('Cannot create a database in a database')

        url = Database(parent_instance.id)._endpoint('databases')
        new_db = Database(parent_instance.id)._post(url, payload=payload)
        new_db_id = new_db.get('id')
        assert new_db_id is not None

        return cls(new_db_id)

    @cached_property
    def retrieve(self) -> JSONObject:
        """Retrieves a Database object using the ID specified. 
        https://developers.notion.com/reference/retrieve-a-database
        """
        url =super()._endpoint('databases', object_id=self.id)
        return super()._get(url)

    @cached_property
    def property_schema(self) -> JSONObject:
        return self.retrieve['properties']

    @property
    def property_names(self) -> list[str]:
        return [key for key in self.retrieve.get('properties').keys()] #type: ignore

    def update(self, payload: JSONObject | JSONPayload) -> JSONObject:
        """Updates an existing database as specified by the parameters.
        https://developers.notion.com/reference/update-a-database
        """
        url = super()._endpoint('databases', object_id=self.id)
        response = super()._patch(url, payload=payload)
        database_logger.info(f"{self.__repr__()} updated \n`{payload!r}`".format(payload))
        return response

    def delete_property(self, name_or_id: str) -> None:
        """Delete a property by either the property name or id. 
        This can be found in the schema with Database.retrieve() 
        """
        payload = {'properties':{name_or_id:None}}
        self.update(payload=payload)
        database_logger.info(f'{self.__repr__()} deleted property `{name_or_id}`')
    
    def rename_property(self, old_name: str, new_name: str) -> None:
        """Rename a property by either the property name or id. 
        This can be found in the schema with Database.retrieve() 
        """
        payload = {'properties':{old_name:{'name':new_name}}}
        self.update(payload=payload)
        database_logger.info(f'{self.__repr__()!r} renamed property `{old_name}` to {new_name}')

    def query(self, payload: JSONObject | JSONPayload | None = None) -> JSONObject:
        """Gets a list of Pages contained in the database, filtered/ordered 
        to the filter conditions/sort criteria provided in request. 
        The response may contain fewer than page_size of results. 
        Responses from paginated endpoints contain a `next_cursor` property, 
        which can be used in a query payload to continue the list.

        NOTE: page_size Default: 100 page_size Maximum: 100.
        https://developers.notion.com/reference/update-a-database 
        """
        url = super()._endpoint('databases', query=True, object_id=self.id)
        return super()._post(url, payload=payload)
