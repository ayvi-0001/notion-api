import typing
import abc

__all__: typing.Sequence[str] = (
    'PagePropertyValue', 
    'PropertyObject', 
    'JSONObject',
    'JSONArray',
    'JSONPayload',
    'JSON',
)


JSONObject = typing.Mapping[str, typing.Any]
JSONArray = typing.Sequence[typing.Any]
JSONPayload = typing.Union[typing.Iterable[bytes], str, bytes]
JSON = typing.Union[str, int, float, bool, JSONArray, JSONObject, None]

class PropertyObject(metaclass=abc.ABCMeta): 
    def __init__(self, property_name: str) -> None:
        self.name = property_name

class PagePropertyValue(metaclass=abc.ABCMeta):
    def __init__(self, property_name: str) -> None:
        self.name = property_name
