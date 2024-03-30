import json
import re
from contextlib import suppress
from typing import Final, Pattern, Sequence, cast

import requests

from notion.api._about import __package_json__, __package_url__, __version__
from notion.api.client import _NLOG

__all__: Sequence[str] = ("check_for_pkg_update",)


def get_version(pkg: str) -> str:
    return str(json.loads(requests.get(pkg).text)["info"]["version"])


def check_for_pkg_update() -> bool | None:
    with suppress(Exception):
        pkg_expr: Final[Pattern[str]] = re.compile(r"(\d).(\d)+.(\d)+", re.I)

        vPYPI = cast(re.Match[str], pkg_expr.match(get_version(__package_json__)))
        vPKG = cast(re.Match[str], pkg_expr.match(__version__))

        pypi_major, pypi_minor, pypi_patch = vPYPI.group(1, 2, 3)
        pkg_major, pkg_minor, pkg_patch = vPKG.group(1, 2, 3)

        pypi_version = int(pypi_major), int(pypi_minor), int(pypi_patch)
        local_version = int(pkg_major), int(pkg_minor), int(pkg_patch)

        if local_version < pypi_version:
            _NLOG.info(
                f" New package version available: {'.'.join(map(str, pypi_version))}. "
                "Run pip install -U notion-api. "
                f"{__package_url__}"
            )

        return local_version < pypi_version
    return None
