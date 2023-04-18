


```py
from datetime import datetime
from datetime import timedelta

from notion import query

TODAY = datetime.combine(datetime.today(), datetime.min.time())
TOMORROW = TODAY + timedelta(1)

query_filter = query.CompoundFilter()._and(
    query.PropertyFilter.date("date", "created_time", "on_or_after", TODAY.isoformat()),
    query.PropertyFilter.date("date", "created_time", "before", TOMORROW.isoformat()),
    query.CompoundFilter()._or(
        query.PropertyFilter.text("name", "title", "contains", "your page title"),
        query.PropertyFilter.text("name", "title", "contains", "your other page title"),
    ),
)

query_sort = query.SortFilter(
    [
        query.PropertyValueSort.ascending("your property name"),
        query.EntryTimestampSort.created_time_descending(),
    ]
)

query_result = new_database.query(
    filter=query_filter,
    sort=query_sort,
    page_size=5,
    filter_property_values=["name", "options"],
)
```