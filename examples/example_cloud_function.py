import os
from datetime import datetime

import functions_framework
from flask import Request
import notion

# Set NOTION_TOKEN and database ID's as env variables.

@functions_framework.http
def main(request: Request) -> str:
    # Setup databases.
    DATABASE_A1 = notion.Database(os.environ["DATABASE_A1_ID"])
    DATABASE_B1 = notion.Database(os.environ["DATABASE_B1_ID"])
    DATABASE_B2 = notion.Database(os.environ["DATABASE_B2_ID"])

    date = str(datetime.today().astimezone(DATABASE_A1.tz).date())

    # Create a page in main database.
    page_A1 = notion.Page.create(DATABASE_A1, page_title=date)

    # Create a page in a 2nd database and relate it to main.
    page_B1 = notion.Page.create(DATABASE_B1, page_title=date)
    page_A1.set_related("related-B1", [page_B1.id])

    # Create a page in a 3rd database and relate it to the 2nd.
    page_B2 = notion.Page.create(DATABASE_B2, page_title=date)
    page_B1.set_related("related-B2", [page_B2.id])

    return "Done"
