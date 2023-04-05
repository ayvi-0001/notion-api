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

from typing import Any, MutableMapping, Optional, Sequence, Union, cast

from notion.api._about import __base_url__
from notion.api.client import _NotionClient
from notion.api.notionblock import Block
from notion.api.notionpage import Page
from notion.exceptions.errors import NotionInvalidRequestUrl, NotionObjectNotFound
from notion.properties.build import NotionObject, build_payload
from notion.properties.common import Parent, UserObject
from notion.properties.richtext import Mention, RichText
from notion.query.sort import EntryTimestampSort, SortFilter

__all__: Sequence[str] = ["Workspace"]


class Workspace(_NotionClient):
    """
    Workspace class is to provide general methods that are not specific to a single object.
    Post/retrieve comments, retrieve users/bots, and search for pages/databases.
    """

    def __init__(
        self,
        token: Optional[str] = None,
    ) -> None:
        super().__init__(token=token)

    def __repr__(self) -> str:
        return f"notion.{self.__class__.__name__}()"

    @staticmethod
    def _workspace_endpoint(
        *,
        users: Optional[bool] = False,
        search: Optional[bool] = None,
        user_id: Optional[str] = None,
        me: Optional[bool] = None,
    ) -> str:
        return "%s%s%s%s%s" % (
            __base_url__,
            "search" if search else "",
            "users" if users else "",
            f"/{user_id}" if user_id else "",
            "/me" if me else "",
        )

    @staticmethod
    def _comments_endpoint(
        *,
        block_id: Optional[str] = None,
        page_size: Optional[int] = None,
        start_cursor: Optional[str] = None,
    ) -> str:
        return "%scomments%s%s%s" % (
            __base_url__,
            f"?block_id={block_id}" if block_id else "",
            f"&page_size={page_size}" if page_size else "",
            f"&start_cursor={start_cursor}" if start_cursor else "",
        )

    def retrieve_token_bot(self) -> MutableMapping[str, Any]:
        """
        Retrieves the bot User associated with the API token provided in the authorization header.
        The bot will have an owner field with information about the person who authorized the integration.

        https://developers.notion.com/reference/get-self
        """
        return self._get(self._workspace_endpoint(users=True, me=True))

    def list_all_users(
        self, *, page_size: Optional[int] = None, cursor: Optional[str] = None
    ) -> MutableMapping[str, Any]:
        """
        Returns a paginated list of Users for the workspace.
        https://developers.notion.com/reference/get-users
        """
        if any([page_size, cursor]):
            payload: dict[str, Any] = {}
            if page_size:
                payload |= {"page_size": page_size}
            if cursor:
                payload |= {"next_cursor": cursor}

            return self._get(self._workspace_endpoint(users=True), payload=payload)

        return self._get(self._workspace_endpoint(users=True))

    def retrieve_user(
        self, *, user_name: Optional[str] = None, user_id: Optional[str] = None
    ) -> UserObject:
        """
        Retrieves a User using either the user name or ID specified.

        :param user_name: (1 of user_name or user_id required) User name in Notion.
        :param user_id: (1 of user_name or user_id required) Identifier for a Notion user

        https://developers.notion.com/reference/get-users
        """
        if not any([user_name, user_id]):
            raise ValueError("Must input either user_name or user_id.")

        if user_name:
            all_users = {
                n.get("name"): n.get("id")
                for n in self.list_all_users().get("results", [])
            }
            if set([user_name]).issubset(all_users):
                user_id = cast(str, all_users.get(user_name))

        user = self._get(self._workspace_endpoint(users=True, user_id=user_id))

        if user["type"] == "bot":
            raise TypeError("User is a bot. Use retrieve_token_bot() instead.")

        try:
            return UserObject(
                id=user["id"],
                name=user["name"],
                avatar_url=user["avatar_url"] if user["avatar_url"] else None,
                email=user["person"]["email"] if user["person"]["email"] else None,
            )
        except KeyError:
            raise NotionObjectNotFound(
                "%s. %s"
                % (
                    f"{self.__repr__()}: Could not find user with name: {user_name}",
                    f"Only members and guests in the integration's workspace are visible.",
                )
            )

    def retrieve_comments(
        self,
        *,
        thread: Union[Page, Block, str],
        page_size: Optional[int] = None,
        start_cursor: Optional[str] = None,
    ) -> MutableMapping[str, Any]:
        """
        When retrieving comments, one or more Comment objects will be returned in the form of an array,
        sorted in ascending chronological order.

        Retrieving comments from a page parent will return all comments on the page, but not
        comments from any blocks inside the page.

        https://developers.notion.com/reference/retrieve-a-comment
        """
        if isinstance(thread, Page) or isinstance(thread, Block):
            block_id = thread.id
        else:
            block_id = thread

        return self._get(
            self._comments_endpoint(
                block_id=block_id, page_size=page_size, start_cursor=start_cursor
            )
        )

    def comment(
        self,
        *,
        page: Optional[Union[Page, Block, str]] = None,
        block: Optional[Union[Block, str]] = None,
        discussion_id: Optional[str] = None,
        comment: Sequence[Union[RichText, Mention]],
    ) -> Union[MutableMapping[str, Any], None]:
        """
        There are two locations you can add a new comment to:
         - A page
         - An existing discussion thread
        Currently the API does not support starting a new comment thread on a block inside a page.
        Comments added will always appear as the newest comment in the thread.

        ---
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
        :param comment: (required) either a Richtext/Mention object.

        https://developers.notion.com/reference/create-a-comment
        """
        if len([k for k, v in locals().items() if v is not None]) > 3:
            raise ValueError("Only one of page/block/discussion_id can be provided.")

        comment_object: NotionObject = NotionObject()
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
                comment_thread = self.retrieve_comments(thread=block.id).get("results")
            else:  # if str of block.id
                comment_thread = self.retrieve_comments(thread=block).get("results")

            if not comment_thread:
                raise ValueError(
                    "%s %s"
                    % (
                        "Did not find a comment thread in this block.",
                        f"Starting new comment threads on a block not supported.",
                    )
                )
            # Regardless of which discussion_id in a comment thread is used,
            # The next comment will always appear last, so we only get the first discussion_id.
            thread_id = comment_thread[0]["discussion_id"]
            payload = build_payload({"discussion_id": thread_id}, comment_object)
            return self._post(self._comments_endpoint(), payload=payload)

        if discussion_id:
            payload = build_payload({"discussion_id": discussion_id}, comment_object)
            return self._post(self._comments_endpoint(), payload=payload)

        raise NotionInvalidRequestUrl(
            "Either a parent page/block, or a discussion_id is required (not both)"
        )

    def search(
        self,
        *,
        page_size: Optional[int] = 100,
        query: Optional[str] = None,
        filter_pages: Optional[bool] = False,
        filter_databases: Optional[bool] = False,
        start_cursor: Optional[str] = None,
        sort_ascending: Optional[bool] = None,
    ) -> MutableMapping[str, Any]:
        """
        ### Searches all original pages, databases, and child pages/databases that are shared with the integration.
        It will not return linked databases, since these duplicate their source databases.
        The response may contain fewer than page_size of results.
        See Pagination in api docs for details about how to use a cursor to iterate through the list.

        ---------------
        ### Limitations of search
        The search endpoint works best when it's being used to query for pages and databases by name.
        It is not optimized for the following use cases:
         - Exhaustively enumerating through all the documents a bot has access to in a workspace.
           Search is not guaranteed to return everything, and the index may change as your integration
           is iterating through pages and databases resulting in unstable results.
         - Searching or filtering within a particular database.
           This use case is much better served by finding the database ID and using the Query a database endpoint.
         - Immediate and complete results. Search indexing is not immediate.
           If an integration performs a search quickly after a page is shared with the integration
           (such as immediately after a user performs OAuth), the response may not contain the page.
         - When an integration needs to present a user interface that depends on search results,
           we recommend including a Refresh button to retry the search.
           This will allow users to determine if the expected result is present or not, and give them a means to try again.

        ---------------
        ### Optimizations and recommended ways to use search
         - Search tends to work best when the request is as specific as possible.
         - Where possible, we recommend filtering by object (such as page or database) and providing a text query to help narrow down results.
         - If search is very slow, specifying a smaller page_size can help. (The default page_size is 100.)
         - Our implementation of the search endpoint includes an optimization where any pages or databases that are
           directly shared with a bot (rather than shared via an ancestor) are guaranteed to be returned.
         - If your use case requires pages or databases to immediately be available in search without an indexing delay,
           we recommend that you share relevant pages/databases with your integration directly.

        ---------------
        #### Search Filter Object
        Limitation: Currently the only filter allowed is object which will filter by type of object
        (either page or database)

        ---------------
        #### Parameters
        :param page_size: (optional) The number of items from the full list desired in the response. Maximum/Default: 100
        :param query: (optional) When supplied, limits which pages are returned by comparing the query to the page title.\
                       If the query parameter is not provided, the response will contain all pages (and child pages) in the results.
        :param filter_pages: (optional) sets the `value` key in the Search Filter object to `page`
        :param filter_databases:(optional)  sets the `value` key in the Search Filter object to `database`
        :param sort_ascending: (optional) Limitation: Currently only a single sort is allowed and\
                                is limited to last_edited_time. The default sort is by last_edited_time descending.\
                                If sort_ascending is set to `True`, the default sort will be overridden.
        :param start_cursor: (optional) If supplied, will return a page of results starting after provided cursor.

        https://developers.notion.com/reference/post-search
        """
        payload = NotionObject()
        payload.set("page_size", page_size)
        if query:
            payload.set("query", query)
        if filter_pages:
            payload.nest("filter", "property", "object")
            payload.nest("filter", "value", "page")
        if filter_databases:
            payload.nest("filter", "property", "object")
            payload.nest("filter", "value", "database")
        if start_cursor:
            payload.set("start_cursor", start_cursor)
        if sort_ascending:
            payload |= SortFilter([EntryTimestampSort.last_edited_time_ascending()])

        return self._post(self._workspace_endpoint(search=True), payload=payload)
