import re
from types import ModuleType
from typing import Final, Pattern, Sequence, Union

import requests

from notion.api._about import *
from notion.api.client import _NLOG

try:
    import orjson

    default_json: ModuleType = orjson
except ModuleNotFoundError:
    import json

    default_json: ModuleType = json


__all__: Sequence[str] = ["inspect_pkg_version"]


def inspect_pkg_version() -> Union[bool, None]:
    expr: Final[Pattern[str]] = re.compile(r"(\d).(\d)+.(\d)+", re.I)

    __package_info__ = default_json.loads(requests.get(__package_json__).text)

    try:
        vPYPI = expr.match(__package_info__["info"]["version"])
        vPKG = expr.match(__version__)

        assert vPYPI and vPKG
        (pypi_major, pypi_minor, pypi_patch) = vPYPI.group(1, 2, 3)
        (pkg_major, pkg_minor, pkg_patch) = vPKG.group(1, 2, 3)
        current_version = (int(pypi_major), int(pypi_minor), int(pypi_patch))
        package_version = (int(pkg_major), int(pkg_minor), int(pkg_patch))

        version_update = package_version < current_version

        if version_update:
            _NLOG.info(
                "Newer package version available: %s - %s"
                % (".".join(map(str, current_version)), __package_url__)
            )

        return version_update
    except KeyError as e:
        _NLOG.error("Unable to check package version: KeyError %s" % e)
        return None
