import typing
import abc

__all__: typing.Sequence[str] = (
    'PagePropertyValue', 
    'PropertyObject', 
    'BlockTypeObjects',
    'DateISO8601',
    'JSONObject',
    'JSONArray',
    'JSONish',
    'JSONPayload'
    )

class PropertyObject(metaclass=abc.ABCMeta): ...
class PagePropertyValue(metaclass=abc.ABCMeta): ...
class BlockTypeObjects(metaclass=abc.ABCMeta): ...

class DateISO8601(typing.Protocol):
    def isoformat(self, sep='T', timespec='auto') -> str: ...

JSONObject = typing.Mapping[str, typing.Any]
JSONArray = typing.Sequence[typing.Any]
JSONPayload = typing.Union[typing.Iterable[bytes], str, bytes]
JSONish = typing.Union[str, int, float, bool, JSONArray, JSONObject, None]
