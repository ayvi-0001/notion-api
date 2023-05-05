## Examples: Retrieving Property Items

```py
import notion

# Set `NOTION_TOKEN` as env var.

home_page = notion.Page("7750e01edd574e2ea81b21d19e46c1f1")
```

Page properties can be retrieved 1 of 2 ways;
    - as property values.
    - as property items.

Our home page has the rich text property type "Welcome Message" 

<p align="center">
    <img src="https://github.com/ayvi-0001/notion-api/blob/main/examples/images/welcome-message.png?raw=true">
</p>


This wrapper supports accessing property values by indexing a page with the name of the property

```py
>>> home_page["Welcome Message"]
```

This returns the property from the property value endpoint.

```json
{
    "id": "itKs",
    "type": "rich_text",
    "rich_text": [
        {
            "type": "text",
            "text": {
                "content": "hello world.",
                "link": null
            },
            "annotations": {
                "bold": false,
                "italic": false,
                "strikethrough": false,
                "underline": false,
                "code": false,
                "color": "default"
            },
            "plain_text": "hello world.",
            "href": null
        }
    ]
}
```

It can also be accessed from the property item endpoint,

```py
>>> home_page.retrieve_property_item("Welcome Message")
```

```json
{
    "object": "list",
    "results": [
        {
            "object": "property_item",
            "type": "rich_text",
            "id": "itKs",
            "rich_text": {
                "type": "text",
                "text": {
                    "content": "hello world.",
                    "link": null
                },
                "annotations": {
                    "bold": false,
                    "italic": false,
                    "strikethrough": false,
                    "underline": false,
                    "code": false,
                    "color": "default"
                },
                "plain_text": "hello world.",
                "href": null
            }
        }
    ],
    "next_cursor": null,
    "has_more": false,
    "type": "property_item",
    "property_item": {
        "id": "itKs",
        "next_url": null,
        "type": "rich_text",
        "rich_text": {}
    }
}
```

This library provides several helper functions to easily retrieve these values.

Property items can also be accessed as attributes.  
Use the same name as in Notion, except replace all non-alphanumeric characters with `_`.  
This returns a `PropertyItem` class that is used by the helper functions.

Then import the `propertyitems` module, and use the appropriate functions to retrieve the value you are looking for.

```py
from notion import propertyitems

# "Welcome Message" becomes "welcome_message"
message: str = propertyitems.rich_text(home_page.welcome_message)
```

```py
>>> hello world.
```

The available functions are:
- `checkbox`
- `number`
- `date`
- `select`
- `multi_select`
- `status`
- `rich_text`
- `number_formula`
- `string_formula`
- `boolean_formula`
- `date_formula`
- `people`
- `email`
- `phone_number`
- `url`
- `files`
- `created_time`
- `created_by`
- `last_edited_time`
- `last_edited_by`
- `relation`
- `number_rollup`
- `date_rollup`

If you prefer to handle the responses another way, the property value and property item methods will always remain available to return the raw responses.

---

### Example: Relation

We have 2 databases related to each other, `Database A` and `Database B`

<p align="center">
    <img src="https://github.com/ayvi-0001/notion-api/blob/main/examples/images/related-page-ids.png?raw=true">
</p>


To get the ID's of the pages in `Database B` that are related to the page `home-page` in `Database A`

```py
home_page = notion.Page("20d9ecd7e0c3442b9cd4696a97fca1e2")

related_page_ids: list[str] = propertyitems.relation(page.related_database_b)
```
```py
>>> ['ea84e68e-8e2e-495d-bb61-8db827d11850', 'c4c7bbba-0433-4e5f-b4ae-b222e0aecf21', '2ada2b98-e44e-4c5b-969a-e17f3ee38624']
```

---

### Example: Rollup | Limitations (Unsupported functions/types)

There are some limitations, for example `percent-per-group` and `count-per-group` are currently unsupported as rollup types.

```json
{
    "object": "list",
    "results": [
        {
            "object": "property_item",
            "type": "status",
            "id": "D%7C%3F%7C",
            "status": {
                "id": "c228f10f-9ff8-43e4-aff2-cd2496a2d661",
                "name": "Not started",
                "color": "red"
            }
        } // ... more status items
    ],
    "next_cursor": null,
    "has_more": false,
    "type": "property_item",
    "property_item": {
        "id": "ne%3B%3F",
        "next_url": null,
        "type": "rollup",
        "rollup": {
            "type": "unsupported", // <--
            "unsupported": {},
            "function": "count_per_group"
        }
    }
}
```

But say we wanted to calculate the percent per group for a status property. We can set up our database as follows:

<p align="center">
    <img src="https://github.com/ayvi-0001/notion-api/blob/main/examples/images/status-view.png?raw=true">
</p>

We can add a formula to `Database B` that returns `true` if the status contains `In progress`.


<p align="center">
    <img src="https://github.com/ayvi-0001/notion-api/blob/main/examples/images/status-formula.png?raw=true">
</p>


Then setup a rollup property aggregating the `if in-progress` property from the relation `related-database-b`, using the `Percent Checked` calculation.


<p align="center">
    <img src="https://github.com/ayvi-0001/notion-api/blob/main/examples/images/status-rollup.png?raw=true">
</p>

Since we are returning a percent, the rollup type is `number`, so we can use the `propertyitems.number_rollup()` function.

```py
percent_in_progress: float = propertyitems.number_rollup(home_page.in_progress)
```
```py
>>> 0.6666666666666666
```

> Other unsupported types by the current version of the Notion API:
> - `show_unique`
> - `median`
>
> The function `show_original` is not implemented in this library yet, but will be once I handle pagination.

---

### Example: Date

Date properties in Notion always include a `start` date. If the date is a range, then it'll also include an `end` date denoting the end of the range. There is also a `timezone` parameter.


For the example below, the `date-range` rollup is calculating the date range of the `start-date` property for the related pages in `Database B`.

<p align="center">
    <img src="https://github.com/ayvi-0001/notion-api/blob/main/examples/images/date-view.png?raw=true">
</p>

The date property value in `start-date` for `sub-page-C` would look like this,

```json
{
    "id": "mxxt",
    "type": "date",
    "date": {
        "start": "2023-04-01",
        "end": null,
        "time_zone": null
    }
}
```

The `date-range` property in `home-page` would return both a `start` and `end` key.

The helper function for dates will return a single datetime object if the only present key is `start`.
If the `end` key is also present, it will return a tuple of 2 datetime objects, with the first index being the `start`, and the latter the `end`.

```py
from typing import cast

sub_page_c = notion.Page("2ada2b98e44e4c5b969ae17f3ee38624")

# casting datetime here since we know it has no end, and won't be tuple[datetime, datetime].
start_date_C = cast(datetime, propertyitems.date(sub_page_c.start_date))
```
```py
>>> 2023-04-01 00:00:00
```
```py
# since this is a rollup returning a date, we use the `date_rollup` function.
date_range = cast(
    tuple[datetime, datetime], propertyitems.date_rollup(testpageA1.date_range)
)
```
```py
>>> (datetime.datetime(2023, 4, 1, 0, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2023, 4, 30, 0, 0, tzinfo=datetime.timezone.utc))
```
```py
range_start: datetime = date_range[0]
range_end: datetime = date_range[1]
```
```py
>>> 2023-04-01 00:00:00+00:00
>>> 2023-04-30 00:00:00+00:00
```

---



