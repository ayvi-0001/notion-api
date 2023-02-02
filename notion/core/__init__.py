from typing import Sequence
import logging

from notion.core.build import *

logging.basicConfig(level=logging.INFO)

notion_logger = logging.getLogger("notion-api")
page_logger = notion_logger.getChild("notion-page")
database_logger = notion_logger.getChild("notion-database")
block_logger = notion_logger.getChild("notion-block")


__all__: Sequence[str] = (
    "NotionObject", 
    "request_json", 
    "notion_logger", 
    "page_logger", 
    "database_logger", 
    "block_logger", 
    )
