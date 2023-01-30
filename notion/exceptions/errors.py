from typing import Sequence

__all__: Sequence[str] = (
    "_NotionErrors",
    "NotionInvalidJson",
    "NotionInvalidRequestUrl",
    "NotionInvalidRequest",
    "NotionValidationError",
    "NotionMissingVersion",
    "NotionUnauthorized",
    "NotionRestrictedResource",
    "NotionObjectNotFound",
    "NotionConflictError",
    "NotionRateLimited",
    "NotionInternalServerError",
    "NotionServiceUnavailable",
    "NotionDatabaseConnectionUnavailable"
    )


class _NotionErrors(BaseException):
    """Base for an error raised by this API.
    Any exceptions should derive from this.

    More info on Errors and Request Limits at:
    https://developers.notion.com/reference/errors
    https://developers.notion.com/reference/request-limits
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NotionInvalidJson(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 400: The request body could not be decoded as JSON."]


class NotionInvalidRequestUrl(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 400: The request URL is not valid."]


class NotionInvalidRequest(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 400: This request is not supported."]


class NotionValidationError(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 400: The request body does not match the schema for the expected parameters."]


class NotionMissingVersion(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 400: The request is missing the required Notion-Version header. See Versioning."]


class NotionUnauthorized(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 401: The bearer token is not valid."]


class NotionRestrictedResource(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 403: Given the bearer token used, the client doesn't have permission to perform this operation."]


class NotionObjectNotFound(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 404: Given the bearer token used, the resource does not exist. This error can also indicate that the resource has not been shared with owner of the bearer token."]


class NotionConflictError(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 409: The transaction could not be completed, potentially due to a data collision. Make sure the parameters are up to date and try again."]


class NotionRateLimited(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 429: This request exceeds the number of requests allowed. Slow down and try again. More details on rate limits."]


class NotionInternalServerError(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 500: An unexpected error occurred. Reach out to Notion support."]


class NotionServiceUnavailable(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 503: Notion is unavailable. Try again later. This can occur when the time to respond to a request takes longer than 60 seconds, the maximum request timeout."]


class NotionDatabaseConnectionUnavailable(_NotionErrors):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

        self.__notes__ = ["Error 503: Notion's database is unavailable or in an unqueryable state. Try again later."]
