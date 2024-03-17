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

from json import loads
from json.decoder import JSONDecodeError
from typing import Any, MutableMapping, NoReturn, Sequence, cast

from notion.exceptions import errors

__all__: Sequence[str] = ("validate_response",)


def validate_response(request: Any) -> MutableMapping[str, Any] | NoReturn:
    try:
        response = loads(request)
    except JSONDecodeError as e:
        raise ValueError(
            "Response did not return a valid json value:\n"
            f"Error: {e}\n"
            f"Response: {request}"
        )

    if "error" in response.values():
        match response["code"]:
            case "invalid_json":
                raise errors.NotionInvalidJson(response["message"])
            case "invalid_request_url":
                raise errors.NotionInvalidRequestUrl(response["message"])
            case "invalid_request":
                raise errors.NotionInvalidRequest(response["message"])
            case "validation_error":
                raise errors.NotionValidationError(response["message"])
            case "missing_version":
                raise errors.NotionMissingVersion(response["message"])
            case "unauthorized":
                raise errors.NotionUnauthorized(response["message"])
            case "restricted_resource":
                raise errors.NotionRestrictedResource(response["message"])
            case "object_not_found":
                raise errors.NotionObjectNotFound(response["message"])
            case "conflict_error":
                raise errors.NotionConflictError(response["message"])
            case "rate_limited":
                raise errors.NotionRateLimited(response["message"])
            case "internal_server_error":
                raise errors.NotionInternalServerError(response["message"])
            case "service_unavailable":
                raise errors.NotionServiceUnavailable(response["message"])
            case "database_connection_unavailable":
                raise errors.NotionDatabaseConnectionUnavailable(response["message"])
            case "gateway_timeout":
                raise errors.NotionGatewayTimeout(response["message"])
            case "invalid_grant":
                raise errors.NotionInvalidGrant(response["message"])
            case _:
                raise errors.NotionUnknownError(response)

    return cast(MutableMapping[str, Any], response)
