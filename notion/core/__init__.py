from typing import Sequence
import logging

from notion.core.build import *

logging.basicConfig(level=logging.INFO)

notion_logger = logging.getLogger("notion-api")

__all__: Sequence[str] = ("NotionObject", "request_json")
