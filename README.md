# notion-api

<p align="center">
    <img alt="last commit" src="https://img.shields.io/github/last-commit/ayvi-0001/notion-api?color=%239146ff&style=plastic"></a>
    <a href="https://developers.notion.com/reference/versioning"><img alt="notion versioning" src="https://img.shields.io/static/v1?label=notion-version&message=version-2022--06--28&color=%232e1a00&style=plastic"></a>
    <a href="https://github.com/ayvi-0001/notion-api/blob/main/LICENSE"><img alt="license: MIT" src="https://img.shields.io/static/v1?label=license&message=MIT&color=informational&style=plastic"></a>
    <img alt="code style: black" src="https://img.shields.io/static/v1?label=code%20style&message=black&color=000000&style=plastic"></a>
</p>

 
A wrapper for Notion's API, aiming to simplify the dynamic nature of interacting with Notion.  

This project is still a work in progress, and features will continue to change. Below are a few examples of the current functionality. 

---
```py
import dotenv

import notion

dotenv.load_dotenv() 
# client will check .env for 'NOTION_TOKEN',

homepage = notion.Page('773b08ff38b44521b44b115827e850f2')
parent_db = notion.Database(homepage.parent_id)

homepage['dependencies']
# {
#     "id": "WYYq",
#     "type": "relation",
#     "relation": [
#         {
#             "id": "7bcbc8e6-e237-434b-bd0d-6b56e044200b"
#         }
#     ],
#     "has_more": false
# }

parent_db['dependencies']
# {
#     "id": "WYYq",
#     "name": "dependencies",
#     "type": "relation",
#     "relation": {
#         "database_id": "f5984a7e-2257-4ab0-9d0a-23ea12324031",
#         "type": "dual_property",
#         "dual_property": {
#             "synced_property_name": "blocked",
#             "synced_property_id": "wx%7DQ"
#         }
#     }
# }

homepage.last_edited.date() # out: 01/15/2023
homepage.title = "New Page Title"
```

---
## Creating Pages/Databases/Blocks
Pages and Databases are created by passing an existing page/database instance as a parent to a classmethod.

```py
new_database = notion.Database.create(
    homepage, database_title="A new database", name_column="name"
)
new_page = notion.Page.create(new_database, page_title="A new database row")
```

Blocks can be created with `notion.api.blocktypefactory.BlockFactory` by appending to an exisiting Block or Page.
```py
import notion.properties as prop

# BlockFactory returns the new block as a Block object.
original_synced_block = notion.BlockFactory.new_synced_block(homepage)

# Adding content to the synced block
notion.BlockFactory.paragraph(original_synced_block, [prop.RichText('This is a synced block.')])

# Referencing the synced block in a new page.
notion.BlockFactory.reference_synced_block(new_page, original_synced_block.id)
```

### Example function: Appending blocks to a page as a reminder.
```py
def notion_block_reminder(page_id: str, message: str, user_name: str) -> None:
    target_page = notion.Page('0b9eccfa890e4c3390175ee10c664a35')
    mentionblock = notion.BlockFactory.paragraph(
        target_page,
        [
            prop.Mention.user(
                notion.Workspace.retrieve_user(user_name=user_name),
                annotations=prop.Annotations(
                    code=True, bold=True, color=prop.NotionColors.purple
                ),
            ),
            prop.RichText(" - "),
            prop.Mention.date(
                datetime.now().astimezone(target_page.tz).isoformat(),
                annotations=prop.Annotations(
                    code=True, bold=True, color=prop.NotionColors.purple_background
                ),
            ),
            prop.RichText(":"),
        ],
    )
    notion.BlockFactory.paragraph(mentionblock, [prop.RichText(message)])
    notion.BlockFactory.divider(target_page)
```

<p align="center">
    <img src="https://raw.githubusercontent.com/ayvi-0001/notion-api/main/images/example_function_reminder.png">  
</p>

---
## Add, Set, & Delete - Page property values / Database property objects

```py
new_database.add_formula_column("page id", expression="id()")

new_database.delete_property("url")

new_database.add_multiselect_column(
    "options",
    options=[
        prop.Option("option-a", prop.PropertyColors.red),
        prop.Option("option-b", prop.PropertyColors.green),
        prop.Option("option-c", prop.PropertyColors.blue),
    ],
)

new_page.set_multiselect("options", ["option-a", "option-b"])
```

---
## Database Queries

```py
from notion.query import *
from datetime import timedelta

# Compound filters support combining `and`/`or` filters.
# Or a single `notion.query.propfilter.PropertyFilter` can be used.

today = datetime.today().isoformat()
tomorrow = (datetime.today() + timedelta(1)).isoformat()

query_filter = notion.build_payload(
    CompoundFilter()._and(
        PropertyFilter.date("date", "date", "on_or_after", today),
        PropertyFilter.date("date", "date", "before", tomorrow),
        CompoundFilter()._or(
            PropertyFilter.text("name", "title", "contains", "your page title"),
            PropertyFilter.text("name", "title", "contains", "your other page title"),
        ),
    ),
    SortFilter([EntryTimestampSort.created_time_descending()]),
)

query_result = new_database.query(
    payload=query_params,
    # Can filter property values returned with a list of property names
    filter_property_values=["name", "options"],
)
```
---

## Exceptions & Validating Responses

```py
# Errors in Notion requests return an object with the keys: 'object', 'status', 'code', and 'message'

homepage._patch_properties(payload={'an_incorrect_key':'value'})
# Example error object for line above..
# {
#   'object': 'error', 
#   'status': 400, 
#   'code': 'validation_error', 
#   'message': 'body failed validation: body.an_incorrect_key should be not present, instead was `"value"`.'
# }
```

```sh
Traceback (most recent call last):
File "c:\path\to\file\_.py", line 6, in <module>
    homepage._patch_properties(payload={'an_incorrect_key':'value'})
File "c:\...\notion\exceptions\validate.py", line 48, in validate_response
    raise NotionValidationError(message)
notion.exceptions.errors.NotionValidationError: body failed validation: body.an_incorrect_key should be not present, instead was `"value"`.
Error 400: The request body does not match the schema for the expected parameters.
```

A common error to look out for is `notion.exceptions.errors.NotionObjectNotFound`  

This error is often raised because your bot has not been added as a connection to the page.  

<p align="center">
    <img src="https://raw.githubusercontent.com/ayvi-0001/notion-api/main/images/directory_add_connections.png">  
</p>

By default, a bot will have access to the children of any Parent object it has access too.

Certain errors are returned with a long list of possible causes for failing validation,
In these cases, the error is often the outlier in the list - for example:

<p align="center">
    <img src="https://raw.githubusercontent.com/ayvi-0001/notion-api/main/images/append_child_block_error.png"> 
</p>

---