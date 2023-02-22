import typing
from typing import Optional
from operator import methodcaller

from jsonpath_ng.ext import parse

from notion.api._about import *
from notion.core.typedefs import *
from notion.exceptions.errors import NotionInvalidRequestUrl
from notion.api.client import _NotionClient
from notion.core.build import NotionObject
from notion.query.sort import SortFilter
from notion.query.sort import EntryTimestampSort

__all__: typing.Sequence[str] = ['Workspace']


class Workspace(_NotionClient):
    """ `notion.api.notionworkspace.Workspace` uses all static methods and doesn't require an instance. """
    def __init__(
        self, *, 
        token: Optional[str] = None, 
        notion_version: Optional[str] = None
    ) -> None:
        super().__init__(token=token, notion_version=notion_version)

    NotionEndpoint: typing.TypeAlias = str
    @staticmethod
    def _workspace_endpoint(
        *, users: Optional[bool] = False, search: Optional[bool] = None,
        user_id: Optional[str] = None, me: Optional[bool] = None
    ) -> NotionEndpoint:
        _search = 'search' if search else ''
        _users = 'users' if users else ''
        _user_id = f'/{user_id}' if user_id else ''
        _me = '/me' if me else ''
        
        return f"{__base_url__}{_search}{_users}{_user_id}{_me}"

    @staticmethod
    def retrieve_token_bot() -> JSONObject:
        """ Retrieves the bot User associated with the API token provided in the authorization header. 
        The bot will have an owner field with information about the person who authorized the integration. 
        
        ---
        https://developers.notion.com/reference/get-self 
        """
        retrieve_token_bot_endpoint = methodcaller('_workspace_endpoint', users=True, me=True)
        url = retrieve_token_bot_endpoint(Workspace())
        return methodcaller('_get', url)(Workspace())
    
    @staticmethod
    def list_all_users(*, page_size: int | None = None, cursor: Optional[str] = None) -> JSONObject:
        """ Returns a paginated list of Users for the workspace. 
        The response may contain fewer than page_size of results.
        
        ---
        https://developers.notion.com/reference/get-users
        """
        payload: typing.MutableMapping = {}
        if page_size:
            payload |= {'page_size':page_size}
        if cursor:
            payload |= {'next_cursor':cursor}
        list_all_users_endpoint = methodcaller('_workspace_endpoint', users=True)
        url = list_all_users_endpoint(Workspace())

        return methodcaller('_get', url)(Workspace())

    @staticmethod
    def retrieve_user(*, user_name: Optional[str] = None,
                         user_id: Optional[str] = None) -> JSONObject:
        """ Retrieves a User using either the user name or ID specified.
        
        ---
        (required) one of the two:
        :param user_name: User name in Notion.
        :param user_id: Identifier for a Notion user
        
        ---
        https://developers.notion.com/reference/get-users
        """

        if user_name:
            try:
                expr = f"$.results[?(@.name=='{user_name}')].id"
                all_users = Workspace.list_all_users()
                user = [m.value for m in parse(expr).find(all_users)][0]
            except IndexError:
                raise NotionInvalidRequestUrl('User name not found.')

            retrieve_user_endpoint = methodcaller(
                '_workspace_endpoint', users=True, user_id=user)
            url = retrieve_user_endpoint(Workspace())
            return methodcaller('_get', url)(Workspace())

        retrieve_user_endpoint = methodcaller(
            '_workspace_endpoint', users=True, user_id=user_id)
        url = retrieve_user_endpoint(Workspace())
        return methodcaller('_get', url)(Workspace())

    @staticmethod
    def search(*, page_size: Optional[int] = 100, 
                  query: Optional[str] = None, 
                  filter_pages: Optional[bool] = False, 
                  filter_databases: Optional[bool] = False,
                  start_cursor: Optional[str] = None,
                  sort_ascending: Optional[bool] = None) -> JSONObject:
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
        :param page_size: (optional) \
             The number of items from the full list desired in the response. Maximum/Default: 100
        :param query: (optional) \
            When supplied, limits which pages are returned by comparing the query to the page title. \
            If the query parameter is not provided, the response will contain all pages (and child pages) in the results.
        :param filter_pages: (optional) sets the `value` key in the Search Filter object to `page`
        :param filter_databases:(optional)  sets the `value` key in the Search Filter object to `database`
        :param sort_ascending: (optional) \
            Limitation: Currently only a single sort is allowed and \
            is limited to last_edited_time. The default sort is by last_edited_time descending. \
            If sort_ascending is set to `True`, the default sort will be overridden.
        :param start_cursor: (optional) \
             If supplied, will return a page of results starting after provided cursor.

        ---
        https://developers.notion.com/reference/post-search
        """
        payload = NotionObject()
        payload.set('page_size', page_size)
        if query:
            payload.set('query', query)
        if filter_pages:
            payload.nest('filter', 'property', 'object')
            payload.nest('filter', 'value', 'page')
        if filter_databases:
            payload.nest('filter', 'property', 'object')
            payload.nest('filter', 'value', 'database')
        if start_cursor:
            payload.set('start_cursor', start_cursor)
        if sort_ascending:
            payload |= SortFilter([EntryTimestampSort.last_edited_time_ascending()])
        
        search_endpoint = methodcaller('_workspace_endpoint', search=True)
        url = search_endpoint(Workspace())
        return methodcaller('_post', url, payload=payload)(Workspace())
