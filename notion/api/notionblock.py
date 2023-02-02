from __future__ import annotations

from typing import  Sequence

from notion.core import *
from notion.properties import *
from notion.exceptions import *
from notion.core.typedefs import *
from notion.api.base_object import _BaseNotionBlock

__all__: Sequence[str] = ["Block"]


class Block(_BaseNotionBlock):
    """ A block object represents content within Notion. 
    Blocks can be text, lists, media, and more. A page is a type of block, too.
    ---
    These are the individual 'nodes' in a page that you typically interact with in Notion.
    Some blocks have more content nested inside them. 
    Some examples are indented paragraphs, lists, and toggles. 
    The nested content is called children, and children are blocks, too.
    ---
    https://developers.notion.com/reference/block 
    """ 
    def __init__(self, id: str, /, *, token: str | None = None, notion_version: str | None = None):
        super().__init__(id, token=token, notion_version=notion_version)

    
    def retrieve(self) -> JSONObject:
        """ Retrieves a Block object using the ID specified.
        https://developers.notion.com/reference/retrieve-a-block 
        """ 
        return self._get(self._block_endpoint(self.id))
    
    def retrievechildren(self) -> JSONObject: #TODO payload for cursor
        """ Returns a paginated array of child block objects contained 
        in the block using the ID specified. 
        In order to receive a complete representation of a block, you 
        may need to recursively retrieve block children of child blocks
        ---
        NOTE: page_size Default: 100 page_size Maximum: 100.

        ---
        https://developers.notion.com/reference/get-block-children
        """ 
        return self._get(self._block_endpoint(self.id, children=True))

    def append_block(self, payload: JSONObject | JSONPayload) -> JSONObject:
        """ Creates/appends new children blocks to the parent 
        block_id specified. Returns a paginated list of newly created 
        children block objects. BODY PARAMS: children | Child 
        content to append to a container block as an array of 
        block objects
        ---
        https://developers.notion.com/reference/patch-block-children 
        """ 
        return self._patch(self._block_endpoint(self.id, children=True), payload=payload)

    def delete_self(self) -> JSONObject:
        """ Sets a Block object, including page blocks, to archived: true 
        using the ID specified. Note: in the Notion UI application, 
        this moves the block to the "Trash" where it can still be 
        accessed and restored. To restore the block with the API, 
        use the Update a block or Update page respectively. 
        ---
        NOTE: To delete a page or database, create a block instance with the respective id,
        and call this method.

        ---
        https://developers.notion.com/reference/delete-a-block
        """ 
        return self._delete(self._block_endpoint(self.id))

    def restore_self(self) -> JSONObject:
        """ Sets "archived" key to false. 
        Only works if the parent page has not been deleted from the trash.
        """ 
        return self._patch(self._block_endpoint(self.id), payload=(b'{"archived": false}'))

    def delete_child(self, children_id: list[str]) -> None:
        for id in children_id:
            self._delete(self._block_endpoint(self.id))
            block_logger.info(f"{self.__repr__()} deleted child block {id}")

    def restore_child(self, children_id: str) -> None:
        for id in children_id:
            self._patch(self._block_endpoint(self.id), payload=b'{"archived": false}')
            block_logger.info(f"{self.__repr__()} restored child block {id}")

    def update(self, payload: JSONObject | JSONPayload) -> JSONObject:
        """ Updates content for the specified block_id based on the block 
        type. Supported fields based on the block object type. 
        Note: The update replaces the entire value for a given field. 
        If a field is omitted (ex: omitting checked when updating a 
        to_do block), the value will not be changed. 

        To update title of a child_page block, use the pages endpoint
        To update title of a child_database block, use the databases endpoint
        To update toggle of a heading block, you can include the optional is_toggleable property in the request 

        Toggle can be added and removed from a heading block. However, 
        you cannot remove toggle from a heading block if it has children
        All children MUST be removed before revoking toggle from a heading block

        ---
        https://api.notion.com/v1/blocks/{block_id} 
        """ 
        return self._patch(self._block_endpoint(self.id), payload=payload)       
