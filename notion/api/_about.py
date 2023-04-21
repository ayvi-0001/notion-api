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

from typing import Final, Sequence

__all__: Sequence[str] = (
    "__content_type__",
    "__notion_version__",
    "__base_url__",
    "__version__",
    "__package_url__",
    "__package_json__",
)

__notion_version__: Final[str] = "2022-06-28"
__content_type__: Final[str] = "application/json"
__base_url__: Final[str] = "https://api.notion.com/v1/"
__version__: Final[str] = "0.4.2"
__package_url__: Final[str] = "https://pypi.org/pypi/notion-api/"
__package_json__: Final[str] = "https://pypi.org/pypi/notion-api/json"


# Notion API Changlog
# https://developers.notion.com/page/changelog

# New changes to notion.so
# https://www.notion.so/releases

# Notion Platform Roadmap
# https://developers.notion.com/page/notion-platform-roadmap

# API Reference
# https://developers.notion.com/reference/intro

# Previous Notion-Version headers
#  - "2021-05-11"
#  - "2021-05-13"
#  - "2021-08-16"
#  - "2022-02-22"
