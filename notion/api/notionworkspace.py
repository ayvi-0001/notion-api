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

from operator import methodcaller
from typing import Any, MutableMapping, Optional, Sequence, TypeAlias, Union, cast

from jsonpath_ng.ext import parse  # type: ignore[import]

from notion.api._about import *
from notion.api._about import __notion_version__
from notion.api.client import _NotionClient
from notion.api.notionblock import Block
from notion.api.notionpage import Page
from notion.exceptions.errors import NotionInvalidRequestUrl, NotionObjectNotFound
from notion.properties.build import NotionObject, build_payload
from notion.properties.common import Parent, UserObject
from notion.properties.richtext import Equation, Mention, RichText
from notion.query.sort import EntryTimestampSort, SortFilter

__all__: Sequence[str] = ["Workspace"]


class Workspace(_NotionClient):
    """`notion.api.notionworkspace.Workspace` uses all static methods and doesn't require an instance."""

    def __init__(
        self, *, token: Optional[str] = None, notion_version: Optional[str] = None
    ) -> None:
        super().__init__(token=token, notion_version=notion_version)

    NotionEndpoint: TypeAlias = str

    @staticmethod
    def _workspace_endpoint(
        *,
        users: Optional[bool] = False,
        search: Optional[bool] = None,
        user_id: Optional[str] = None,
        me: Optional[bool] = None,
    ) -> NotionEndpoint:
        _search = "search" if search else ""
        _users = "users" if users else ""
        _user_id = f"/{user_id}" if user_id else ""
        _me = "/me" if me else ""

        return f"{__base_url__}{_search}{_users}{_user_id}{_me}"

    @staticmethod
    def _comments_endpoint(
        *,
        block_id: Optional[str] = None,
        page_size: Optional[int] = None,
        start_cursor: Optional[str] = None,
    ) -> NotionEndpoint:
        comments = "comments"
        block_id_ = f"?block_id={block_id}" if block_id else ""
        page_size_ = f"&page_size={page_size}" if page_size else ""
        start_cursor_ = f"&start_cursor={start_cursor}" if start_cursor else ""

        return f"{__base_url__}{comments}{block_id_}{page_size_}{start_cursor_}"

    @staticmethod
    def retrieve_token_bot() -> MutableMapping[str, Any]:
        """Retrieves the bot User associated with the API token provided in the authorization header.
        The bot will have an owner field with information about the person who authorized the integration.

        https://developers.notion.com/reference/get-self
        """
        retrieve_token_bot_endpoint = methodcaller(
            "_workspace_endpoint", users=True, me=True
        )
        url = retrieve_token_bot_endpoint(Workspace())
        return cast("MutableMapping[str, Any]", methodcaller("_get", url)(Workspace()))

    @staticmethod
    def list_all_users(
        *, page_size: Optional[int] = None, cursor: Optional[str] = None
    ) -> MutableMapping[str, Any]:
        """Returns a paginated list of Users for the workspace.
        The response may contain fewer than page_size of results.

        https://developers.notion.com/reference/get-users
        """
        payload: dict[str, Any] = {}
        if page_size:
            payload |= {"page_size": page_size}
        if cursor:
            payload |= {"next_cursor": cursor}
        list_all_users_endpoint = methodcaller("_workspace_endpoint", users=True)
        return cast(
            "MutableMapping[str, Any]",
            methodcaller("_get", list_all_users_endpoint(Workspace()))(Workspace()),
        )

    @staticmethod
    def retrieve_user(
        *, user_name: Optional[str] = None, user_id: Optional[str] = None
    ) -> UserObject:
        """Retrieves a User using either the user name or ID specified.

        ---
        :param user_name: (1 of `user_name` or `user_id` required) User name in Notion.
        :param user_id: (1 of `user_name` or `user_id` required) Identifier for a Notion user

        https://developers.notion.com/reference/get-users
        """
        if user_name:
            try:
                user = [
                    m.value
                    for m in parse(f"$.results[?(@.name=='{user_name}')].id").find(
                        Workspace.list_all_users()
                    )
                ][0]
            except IndexError:
                raise NotionInvalidRequestUrl("User name not found.")

            retrieve_user_endpoint = methodcaller(
                "_workspace_endpoint", users=True, user_id=user
            )

        elif user_id:
            retrieve_user_endpoint = methodcaller(
                "_workspace_endpoint", users=True, user_id=user_id
            )

        else:
            raise ValueError("Input either user_name or user_id.")

        user = methodcaller("_get", retrieve_user_endpoint(Workspace()))(Workspace())

        return UserObject(
            id=user["id"],
            name=user["name"],
            avatar_url=user["avatar_url"] if user["avatar_url"] else None,
            email=user["person"]["email"] if user["person"]["email"] else None,
        )

    @staticmethod
    def retrieve_comments(
        *,
        notion_id: Union[Page, Block, str],
        page_size: Optional[int] = None,
        start_cursor: Optional[str] = None,
    ) -> MutableMapping[str, Any]:
        """When retrieving comments, one or more Comment objects will be returned in the form of an array,
        sorted in ascending chronological order.

        retrieving comments from a page parent will return all comments on the page, but not
        comments from any blocks inside the page

        https://developers.notion.com/reference/retrieve-a-comment
        """
        if isinstance(notion_id, str):
            block = notion_id
        else:
            block = notion_id.id

        retrieve_comments_endpoint = methodcaller(
            "_comments_endpoint",
            block_id=block,
            page_size=page_size,
            start_cursor=start_cursor,
        )
        return cast(
            "MutableMapping[str, Any]",
            methodcaller("_get", retrieve_comments_endpoint(Workspace()))(Workspace()),
        )

    @staticmethod
    def comment(
        *,
        page: Optional[Union[Page, Block, str]] = None,
        block: Optional[Union[Block, str]] = None,
        discussion_id: Optional[str] = None,
        rich_text: Sequence[Union[RichText, Mention, Equation]],
    ) -> Union[MutableMapping[str, Any], None]:
        """
        There are two locations you can add a new comment to:
         - A page
         - An existing discussion thread
        Currently the API does not support starting a new comment thread on a block inside a page.
        Comments added will always appear as the newest comment in the thread.

        ---
        :param page: (1 of `page`/`block`/`discussion_id` required)
            either a string representing the id of a page, or an instance
            of `notion.api.notionpage.Page`.
            passing a string id of child block inside a page will raise
            `notion.exceptions.errors.NotionObjectNotFound`
            passing a `notion.api.notionblock.Block` instance to the `page` param
            will create a comment to the parent_id of the block.
        :param block: (1 of `page`/`block`/`discussion_id` required)
            either a string representing the id of a page, or an instance
            of `notion.api.notionblock.Block`.
            Will search the block for an existing discussion thread, and comment in
            that thread if found, else will raise `notion.exceptions.errors.NotionObjectNotFound`
        :param discussion_id: (1 of `page`/`block`/`discussion_id` required)
            a string representing the discussion_id of a comment object.
        :param rich_text: (required) either a `notion.properties.richtext.Richtext` object
            or `notion.properties.richtext.Mention` object.

        https://developers.notion.com/reference/create-a-comment
        """
        retrieve_comments_endpoint = methodcaller(
            "_comments_endpoint",
        )
        comment: NotionObject = NotionObject()
        comment.set("rich_text", rich_text)

        if page:
            if isinstance(page, Page):
                parent_object = Parent.page(page.id)
            elif isinstance(page, Block):
                parent_object = Parent.page(page.parent_id)
            elif isinstance(page, str):
                parent_object = Parent.page(page)

            return cast(
                "MutableMapping[str, Any]",
                methodcaller(
                    "_post",
                    retrieve_comments_endpoint(Workspace()),
                    payload=build_payload(parent_object, comment),
                )(Workspace()),
            )

        if block:
            if isinstance(block, Block):
                comment_thread = Workspace.retrieve_comments(notion_id=block.id)
            else:
                comment_thread = Workspace.retrieve_comments(notion_id=block)

            if not comment_thread.get("results"):
                raise NotionObjectNotFound(
                    (
                        "Did not find a comment thread in this block to add too. ",
                        f"Notion API version {__notion_version__} currently does not ",
                        "Support creating new comment threads on a block.",
                    )
                )
            discussion_thread = {
                # regardless of the discussion_id used in a comment thread on a block,
                # the next comment will always appear last,
                # so only getting first discussion_id.
                "discussion_id": comment_thread.get("results", [])[0].get(
                    "discussion_id"
                )
            }
            return cast(
                "MutableMapping[str, Any]",
                methodcaller(
                    "_post",
                    retrieve_comments_endpoint(Workspace()),
                    payload=build_payload(discussion_thread, comment),
                )(Workspace()),
            )

        if discussion_id:
            return cast(
                "MutableMapping[str, Any]",
                methodcaller(
                    "_post",
                    retrieve_comments_endpoint(Workspace()),
                    payload=build_payload({"discussion_id": discussion_id}, comment),
                )(Workspace()),
            )

        elif not any([page, block, discussion_id]):
            raise NotionInvalidRequestUrl(
                "Either a parent page/block, or a discussion_id is required (not both)"
            )
        return None

    @staticmethod
    def search(
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
        :param page_size: (optional)
             The number of items from the full list desired in the response. Maximum/Default: 100
        :param query: (optional)
            When supplied, limits which pages are returned by comparing the query to the page title.
            If the query parameter is not provided, the response will contain all pages (and child pages) in the results.
        :param filter_pages: (optional) sets the `value` key in the Search Filter object to `page`
        :param filter_databases:(optional)  sets the `value` key in the Search Filter object to `database`
        :param sort_ascending: (optional)
            Limitation: Currently only a single sort is allowed and
            is limited to last_edited_time. The default sort is by last_edited_time descending.
            If sort_ascending is set to `True`, the default sort will be overridden.
        :param start_cursor: (optional)
             If supplied, will return a page of results starting after provided cursor.

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

        return cast(
            "MutableMapping[str, Any]",
            methodcaller(
                "_post",
                methodcaller("_workspace_endpoint", search=True)(Workspace()),
                payload=payload,
            )(Workspace()),
        )
