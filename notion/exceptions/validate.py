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

from typing import Any, MutableMapping, Sequence

from notion.exceptions.errors import (
    NotionConflictError,
    NotionDatabaseConnectionUnavailable,
    NotionGatewayTimeout,
    NotionInternalServerError,
    NotionInvalidJson,
    NotionInvalidGrant,
    NotionInvalidRequest,
    NotionInvalidRequestUrl,
    NotionMissingVersion,
    NotionObjectNotFound,
    NotionRateLimited,
    NotionRestrictedResource,
    NotionServiceUnavailable,
    NotionUnauthorized,
    NotionValidationError,
    _NotionErrors,
)

__all__: Sequence[str] = ["validate_response"]


def validate_response(response: MutableMapping[str, Any]) -> _NotionErrors | None:
    r"""Example:
    >>> page = notion.Page("12345")

    ```json
    // Object for invalid Notion requests:
    {
      "object": "error",
      "status": 400,
      "code": "validation_error",
      "message": "path failed validation: path.page_id should be a valid uuid, instead was `"12345"`."
    }
    ```
    ---
    ```shell
    Traceback (most recent call last):
      File "c:\path\to\file\_.py", line 212, in <module>
        validate_response(response)
      File "c:\path\to\file\_.py", line 186, in validate_response
        raise NotionValidationError(response["message"])
    notion.exceptions.errors.NotionValidationError: path failed validation: path.page_id should be a valid uuid, instead was `"12345"`.
    Error 400:
    The request body does not match the schema for the expected parameters.
    ```

    More info on Errors and Request Limits:
     - https://developers.notion.com/reference/status-codes
     - https://developers.notion.com/reference/request-limits
    """
    if not "error" in response.values():
        return None

    match response["code"]:
        case "invalid_json":
            raise NotionInvalidJson(response["message"])
        case "invalid_request_url":
            raise NotionInvalidRequestUrl(response["message"])
        case "invalid_request":
            raise NotionInvalidRequest(response["message"])
        case "validation_error":
            raise NotionValidationError(response["message"])
        case "missing_version":
            raise NotionMissingVersion(response["message"])
        case "unauthorized":
            raise NotionUnauthorized(response["message"])
        case "restricted_resource":
            raise NotionRestrictedResource(response["message"])
        case "object_not_found":
            raise NotionObjectNotFound(response["message"])
        case "conflict_error":
            raise NotionConflictError(response["message"])
        case "rate_limited":
            raise NotionRateLimited(response["message"])
        case "internal_server_error":
            raise NotionInternalServerError(response["message"])
        case "service_unavailable":
            raise NotionServiceUnavailable(response["message"])
        case "database_connection_unavailable":
            raise NotionDatabaseConnectionUnavailable(response["message"])
        case "gateway_timeout":
            raise NotionGatewayTimeout(response["message"])
        case "invalid_grant":
            raise NotionInvalidGrant(response["message"])
        case _:
            return None
