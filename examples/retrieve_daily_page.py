from datetime import datetime
from datetime import timedelta

import notion
from notion import query


def retrieve_daily_page(database: notion.Database) -> notion.Page:
    """
    This function is meant to be used on a database where you only create a single page per day.
    For example, a daily journal or a daily to-do list.

    Database must have a created_time property in schema.
    Will return the first page in the database that was created today.

    :param database: The database to search.
    :returns: `notion.Page`
    """
    db_schema = database.property_schema.items()

    try:
        # finding the name of the created_time property
        created_property = [k for k, v in db_schema if v["type"] == "created_time"][0]
    except IndexError:
        raise ValueError("Could not find a created_time property in schema.")

    TODAY = datetime.combine(datetime.today(), datetime.min.time())
    TOMORROW = TODAY + timedelta(1)

    query_filter = query.CompoundFilter()._and(
        query.PropertyFilter.date(
            created_property, "created_time", "on_or_after", TODAY.isoformat()
        ),
        query.PropertyFilter.date(
            created_property, "created_time", "before", TOMORROW.isoformat()
        ),
    )

    page = database.query_pages(filter=query_filter, page_size=1)[0]

    return page
