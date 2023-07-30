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

from typing import Sequence

__all__: Sequence[str] = (
    "NotionConflictError",
    "NotionDatabaseConnectionUnavailable",
    "NotionGatewayTimeout",
    "NotionInvalidGrant",
    "NotionInternalServerError",
    "NotionInvalidJson",
    "NotionInvalidRequest",
    "NotionInvalidRequestUrl",
    "NotionMissingVersion",
    "NotionObjectNotFound",
    "NotionRateLimited",
    "NotionRestrictedResource",
    "NotionServiceUnavailable",
    "NotionUnauthorized",
    "NotionValidationError",
    "_NotionErrors",
)


class _NotionErrors(BaseException):
    """Base for an error raised by this API. Any exceptions should derive from this.

    More info on Errors and Request Limits:
     - https://developers.notion.com/reference/status-codes
     - https://developers.notion.com/reference/request-limits
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NotionInvalidJson(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = [
            "Error 400: The request body could not be decoded as JSON."
        ]


class NotionInvalidRequestUrl(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = ["Error 400: The request URL is not valid."]


class NotionInvalidRequest(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = ["Error 400: This request is not supported."]



class NotionInvalidGrant(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = [
            "Error 400: The provided authorization grant (e.g., authorization code, resource owner credentials) or refresh token is", 
            "invalid, expired, revoked, does not match the redirection URI used in the authorization request, or was issued to another client.", 
            "See OAuth 2.0 documentation for more information."
            ]


class NotionValidationError(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = [
            "Error 400: The request body does not match the schema for the expected parameters."
        ]


class NotionMissingVersion(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = [
            "Error 400: The request is missing the required Notion-Version header. See Versioning."
        ]


class NotionUnauthorized(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = ["Error 401: The bearer token is not valid."]


class NotionRestrictedResource(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = [
            "Error 403: Given the bearer token used, "
            "the client doesn't have permission to perform this operation."
        ]


class NotionObjectNotFound(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = [
            "Error 404: Given the bearer token used, the resource does not exist. ",
            "This error can also indicate that the resource has not been shared with owner of the bearer token.",
        ]


class NotionConflictError(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = [
            "Error 409: The transaction could not be completed, potentially due to a data collision. ",
            "Make sure the parameters are up to date and try again.",
        ]


class NotionRateLimited(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = [
            "Error 429: This request exceeds the number of requests allowed. ",
            "Slow down and try again. More details on rate limits.",
        ]


class NotionInternalServerError(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = [
            "Error 500: An unexpected error occurred. Reach out to Notion support."
        ]


class NotionServiceUnavailable(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = [
            "Error 503: Notion is unavailable. Try again later. ",
            "This can occur when the time to respond to a request takes longer than 60 seconds, ",
            "the maximum request timeout.",
        ]


class NotionDatabaseConnectionUnavailable(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = [
            "Error 503: Notion's database is unavailable or in an unqueryable state. Try again later."
        ]


class NotionGatewayTimeout(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.__notes__: list[str] = [
            "Error 504: Notion timed out while attempting to complete this request. Please try again later."
        ]
