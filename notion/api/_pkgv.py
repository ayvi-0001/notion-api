import re
from types import ModuleType
from typing import Callable, Final, Pattern, Sequence, cast

import requests

from notion.api._about import __package_json__, __package_url__, __version__
from notion.api.client import _NLOG

try:
    import orjson

    _json: ModuleType = orjson
except ModuleNotFoundError:
    import json

    _json: ModuleType = json # type: ignore[no-redef]


__all__: Sequence[str] = ["check_for_pkg_update"]


get_version: Callable[[str], str] = lambda pkg: cast(
    str, _json.loads(requests.get(pkg).text)["info"]["version"]
)


def check_for_pkg_update() -> bool | None:
    pkg_expr: Final[Pattern[str]] = re.compile(r"(\d).(\d)+.(\d)+", re.I)

    try:
        vPYPI = cast(re.Match[str], pkg_expr.match(get_version(__package_json__)))
        vPKG = cast(re.Match[str], pkg_expr.match(__version__))

        (pypi_major, pypi_minor, pypi_patch) = vPYPI.group(1, 2, 3)
        (pkg_major, pkg_minor, pkg_patch) = vPKG.group(1, 2, 3)

        pypi_version = (int(pypi_major), int(pypi_minor), int(pypi_patch))
        local_version = (int(pkg_major), int(pkg_minor), int(pkg_patch))

        if local_version < pypi_version:
            _NLOG.info(
                "Newer package version available: %s - %s"
                % (".".join(map(str, pypi_version)), __package_url__)
            )

        return local_version < pypi_version
    except Exception:
        return None
