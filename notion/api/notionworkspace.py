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

from functools import partial, partialmethod
from typing import Any, MutableMapping, Optional, Sequence

from notion.api._about import __base_url__
from notion.api._pagination import paginated_response_endpoint
from notion.api.client import _NLOG, _NotionClient
from notion.api.notionblock import Block
from notion.api.notionpage import Page
from notion.properties.build import NotionObject, build_payload
from notion.properties.common import Parent
from notion.properties.richtext import Mention, RichText
from notion.query.sort import EntryTimestampSort

__all__: Sequence[str] = ("Workspace",)


class Workspace(_NotionClient):
    """The Workspace class is for general methods that are not specific to a single page/database/block object.

    This covers the endpoints:
        - [Users](https://developers.notion.com/reference/get-users)
            - list all users
            - retrieve a user
            - retrieve your token bot's user
        - [Search](https://developers.notion.com/reference/post-search)
            - search workspace by title, page/database objects
        - [Comments](https://developers.notion.com/reference/create-a-comment)
            - create a comment
            - retrieve comments
    """

    def __init__(self, token: Optional[str] = None) -> None:
        super().__init__(token=token)
        self.logger = _NLOG.getChild(repr(self))

    def __repr__(self) -> str:
        return f"notion.Workspace()"

    @staticmethod
    def _workspace_endpoint(
        *,
        users: Optional[bool] = False,
        search: Optional[bool] = None,
        user_id: Optional[str] = None,
        me: Optional[bool] = None,
    ) -> str:
        return "".join(
            [
                __base_url__,
                "search" if search else "",
                "users" if users else "",
                f"/{user_id}" if user_id else "",
                "/me" if me else "",
            ]
        )

    @staticmethod
    def _comments_endpoint(
        *,
        block_id: Optional[str] = None,
        page_size: Optional[int] = None,
        start_cursor: Optional[str] = None,
    ) -> str:
        return "".join(
            [
                __base_url__,
                "comments",
                f"?block_id={block_id}" if block_id else "",
                f"&page_size={page_size}" if page_size else "",
                f"&start_cursor={start_cursor}" if start_cursor else "",
            ]
        )

    def retrieve_token_bot(self) -> MutableMapping[str, Any]:
        """
        Retrieves the bot User associated with the API token provided in the authorization header.
        The bot will have an owner field with information about the person who authorized the integration.

        https://developers.notion.com/reference/get-self
        """
        return self._get(self._workspace_endpoint(users=True, me=True))

    def list_all_users(
        self, *, page_size: Optional[int] = None, next_cursor: Optional[str] = None
    ) -> MutableMapping[str, Any]:
        """
        Returns a paginated list of Users for the workspace.
        https://developers.notion.com/reference/get-users
        """
        payload = NotionObject()

        if page_size or next_cursor:
            if page_size:
                payload.set("page_size", page_size)
            if next_cursor:
                payload.set("next_cursor", next_cursor)

        return self._get(self._workspace_endpoint(users=True), payload=payload)

    def retrieve_user(
        self, *, user_name: Optional[str] = None, user_id: Optional[str] = None
    ) -> MutableMapping[str, Any]:
        """Retrieves a User using either the user name or ID specified.

        :param user_name: (1 of user_name or user_id required) User name in Notion.
        :param user_id: (1 of user_name or user_id required) Identifier for a Notion user

        https://developers.notion.com/reference/get-users
        """
        if not (user_name or user_id):
            raise ValueError("Must input either user_name or user_id.")

        all_users: list[MutableMapping[str, Any]] = self.list_all_users()["results"]

        if user_name:
            for idx, user in enumerate(all_users):
                if user["name"] == user_name:
                    return all_users[idx]
        else:
            for idx, user in enumerate(all_users):
                if user["id"] == user_id:
                    return all_users[idx]

        raise ValueError(
            f"{self}: Could not find user with name: {user_name}. "
            "Only members and guests in the integration's workspace are visible."
        )

    def retrieve_comments(
        self, thread: Page | Block | str, *, max_page_size: Optional[int] = None
    ) -> list[MutableMapping[str, Any]]:
        """
        When retrieving comments, one or more Comment objects will be returned in the form of an array,
        sorted in ascending chronological order.

        Retrieving comments from a page parent will return all comments on the page,
        but not comments from any blocks inside the page.

        :param thread: (required) Either a notion.Page or notion.Block object,
                       or the string of a page/block/discussion_thread ID.
        :param max_page_size: (optional) The max number of pages to include in results.\
                               If left blank, will iterate until all comments in results are included.

        https://developers.notion.com/reference/retrieve-a-comment
        """
        if isinstance(thread, (Page, Block)):
            block_id = thread.id
        else:
            block_id = thread

        return paginated_response_endpoint(
            partialmethod(self._get),
            partial(self._comments_endpoint, block_id=block_id),
            max_page_size,
        )

    def comment(
        self,
        comment: Sequence[RichText | Mention],
        *,
        page: Optional[Page | Block | str] = None,
        block: Optional[Block | str] = None,
        discussion_id: Optional[str] = None,
    ) -> MutableMapping[str, Any] | None:
        """
        Creates a comment in a page or existing discussion thread.
        There are two locations you can add a new comment to:
         - A page
         - An existing discussion thread
        
        If the intention is to add a new comment to a page, a parent object must be provided. 
        Alternatively, if a new comment is being added to an existing discussion thread, the discussion_id string must be provided. 
        **Exactly one** of these parameters must be provided.
        
        Currently the API does not support starting a new comment thread on a block inside a page.
        Comments added will always appear as the newest comment in the thread.
        
        ---
        :param comment: (required) list containing Richtext/Mention objects.
        :param page: (1 of page/block/discussion_id required)\
                      either a string representing the id of a page, or a Page instance.\
                      - passing a string id of child block inside a page will raise NotionObjectNotFound\
                      - passing a Block instance to the page param will create a comment to the parent_id of the block.
        :param block: (1 of page/block/discussion_id required)\
                       either a string representing the id of a block, or a Block instance.\
                       Will search the block for an existing discussion thread,\
                        and comment in that thread if found.
        :param discussion_id: (1 of page/block/discussion_id required)\
                               a string representing the discussion_id of a comment object.

        https://developers.notion.com/reference/create-a-comment
        """
        if len([k for k, v in locals().items() if v is not None]) > 3:
            raise ValueError("Only one of page/block/discussion_id can be provided.")

        comment_object = NotionObject()
        comment_object.set("rich_text", comment)

        if page:
            if isinstance(page, Page):
                payload = build_payload(Parent.page(page.id), comment_object)
            elif isinstance(page, Block):
                payload = build_payload(Parent.page(page.parent_id), comment_object)
            elif isinstance(page, str):
                payload = build_payload(Parent.page(page), comment_object)

            return self._post(self._comments_endpoint(), payload=payload)

        if block:
            if isinstance(block, Block):
                comment_thread = self.retrieve_comments(thread=block.id)
            else:  # if str of block.id
                comment_thread = self.retrieve_comments(thread=block)

            if not comment_thread:
                raise ValueError(
                    "Did not find a comment thread in this block. "
                    "Starting new comment threads on a block not supported."
                )
            # The next comment will always appear last regardless of which discussion_id
            # in a comment thread is used,, so we only get the first discussion_id.
            thread_id = comment_thread[0]["discussion_id"]
            payload = build_payload({"discussion_id": thread_id}, comment_object)
            return self._post(self._comments_endpoint(), payload=payload)

        if discussion_id:
            payload = build_payload({"discussion_id": discussion_id}, comment_object)
            return self._post(self._comments_endpoint(), payload=payload)

        raise ValueError("One of page/block/discussion_id must be provided.")

    def search(
        self,
        query_string: Optional[str] = None,
        *,
        filter_pages: Optional[bool] = False,
        filter_databases: Optional[bool] = False,
        page_size: Optional[int] = 100,
        start_cursor: Optional[str] = None,
        sort_ascending: Optional[bool] = None,
    ) -> MutableMapping[str, Any]:
        """
        Searches all parent or child pages and databases that have been shared with an integration.
        Returns all pages or databases, excluding duplicated linked databases, that have titles that include the query param.
        If no query param is provided, then the response contains all pages or databases that have been shared with the integration.
        The results adhere to any limitations related to an integration's capabilities.
        To limit the request to search only pages or to search only databases, use the filter param.

        For more information on the limitations/optimizations of search,
        see [Search optimizations and limitations](https://developers.notion.com/reference/post-search).

        ---
        :param query_string: (optional) The text that the API compares page and database titles against.
        :param filter_pages: (optional) If set to True, limits results to only `page` objects.
        :param filter_databases:(optional) If set to True, limits results to only `database` objects.
        :param page_size: (optional) The number of items from the full list to include in the response. Maximum: 100. Default: 100.
        :param sort_ascending: (optional) If sort is not provided, then default sort is last_edited_time descending.
        :param start_cursor: (optional) If supplied, will return a page of results starting after provided cursor.

        https://developers.notion.com/reference/post-search
        """
        payload = NotionObject()
        payload.set("page_size", page_size)

        if query_string:
            payload.set("query", query_string)
        if filter_pages:
            payload.nest("filter", "property", "object")
            payload.nest("filter", "value", "page")
        if filter_databases:
            payload.nest("filter", "property", "object")
            payload.nest("filter", "value", "database")
        if start_cursor:
            payload.set("start_cursor", start_cursor)
        if sort_ascending:
            payload.set("sort", EntryTimestampSort.last_edited_time_ascending())

        return self._post(self._workspace_endpoint(search=True), payload=payload)

    def _retrieve_comments(
        self,
        /,
        thread: Page | Block | str,
        *,
        page_size: Optional[int] = None,
        start_cursor: Optional[str] = None,
    ) -> MutableMapping[str, Any]:
        """
        ### This method is deprecated since > v0.5.2.
        It's been replaced with the new retrieve_comments() method that iterates through all results.
        This is the original endpoint and will return a max of 100 pages, and a cursor to use in the next query if the results are greater than 100.

        When retrieving comments, one or more Comment objects will be returned in the form of an array,
        sorted in ascending chronological order.

        Retrieving comments from a page parent will return all comments on the page,
        but not comments from any blocks inside the page.

        :param thread: (required) Either a notion.Page or notion.Block object,
                       or the string of a page/block/discussion_thread ID.

        https://developers.notion.com/reference/retrieve-a-comment
        """
        if isinstance(thread, (Page, Block)):
            block_id = thread.id
        else:
            block_id = thread

        comments_endpoint = self._comments_endpoint(
            block_id=block_id, page_size=page_size, start_cursor=start_cursor
        )
        return self._get(comments_endpoint)
