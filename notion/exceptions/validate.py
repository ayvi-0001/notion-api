from notion.exceptions.errors import *
from notion.core.typedefs import *

import typing

__all__: typing.Sequence[str] = ['validate_response']


def validate_response(response: JSONObject | typing.Mapping[str, typing.Any]) -> _NotionErrors | None:
    r"""
    To be used on response from notion.Page | notion.Database | notion.Block,
    Not for instantiation.

    Example:
    ```py
    page = notion.Page("12345")
    notion.check_exceptions(page.retrieve())

    # Object for invalid Notion requests:
    # { 
    #   'object': 'error', 
    #   'status': 400, 
    #   'code': 'validation_error', 
    #   'message': 'path failed validation: path.page_id should be a valid uuid, instead was `"12345"`.'
    # }

    >>> check_exceptions(response)
    ```
    ---
    ```sh
    Traceback (most recent call last):
      File "c:\path\to\file\_.py", line 212, in <module>
        check_exceptions(response)
      File "c:\path\to\file\_.py", line 186, in check_exceptions
        raise NotionValidationError(message)
    notion.exceptions.errors.NotionValidationError: path failed validation: path.page_id should be a valid uuid, instead was `"12345"`.
    Error 400:
    The request body does not match the schema for the expected parameters.    
    ```
    ---
    https://developers.notion.com/reference/errors
    """
    if 'error' in response.values():
        code = response['code']    
        message = response['message']

        if "invalid_json" in code:
            raise NotionInvalidJson(message)
        if "invalid_request_url" in code:
            raise NotionInvalidRequestUrl(message)
        if "invalid_request" in code:
            raise NotionInvalidRequest(message)
        if "validation_error" in code:
            raise NotionValidationError(message)
        if "missing_version" in code:
            raise NotionMissingVersion(message)
        if "unauthorized" in code:
            raise NotionUnauthorized(message)
        if "restricted_resource" in code:
            raise NotionRestrictedResource(message)
        if "object_not_found" in code:
            raise NotionObjectNotFound(message)
        if "conflict_error" in code:
            raise NotionConflictError(message)
        if "rate_limited" in code:
            raise NotionRateLimited(message)
        if "internal_server_error" in code:
            raise NotionInternalServerError(message)
        if "service_unavailable" in code:
            raise NotionServiceUnavailable(message)
        if "database_connection_unavailable" in code:
            raise NotionDatabaseConnectionUnavailable(message)
    else:
        pass
    return None
