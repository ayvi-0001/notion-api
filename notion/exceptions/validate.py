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

from typing import Any, MutableMapping, Sequence, Union

from notion.exceptions.errors import *

__all__: Sequence[str] = ["validate_response"]


def validate_response(response: MutableMapping[str, Any]) -> Union[_NotionErrors, None]:
    r"""
    To be used on responses from notion.Page, notion.Database, notion.Block.

    Example:
    ```py
    page = notion.Page("12345")

    # Object for invalid Notion requests:
    # {
    #   'object': 'error',
    #   'status': 400,
    #   'code': 'validation_error',
    #   'message': 'path failed validation: path.page_id should be a valid uuid, instead was `"12345"`.'
    # }
    ```
    ------
    ```sh
    Traceback (most recent call last):
      File "c:\path\to\file\_.py", line 212, in <module>
        validate_response(response)
      File "c:\path\to\file\_.py", line 186, in validate_response
        raise NotionValidationError(message)
    notion.exceptions.errors.NotionValidationError: path failed validation: path.page_id should be a valid uuid, instead was `"12345"`.
    Error 400:
    The request body does not match the schema for the expected parameters.
    ```

    https://developers.notion.com/reference/errors
    """
    if "error" in response.values():
        code = response["code"]
        message = response["message"]

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

    return None
