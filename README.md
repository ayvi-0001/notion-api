# notion-wrapper
 
A wrapper for Notion's API, aiming to simplify the dynamic nature of interacting with Notion.  

Current Notion-Version: 2022-06-28.

This is still a work in progress, and features will continue to change.

Here are a few examples so far:  

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
homepage.last_edited.time() # out: 16:28:00
```

---
## Creating Pages/Databases/Blocks
Pages and Databases are created by passing an existing page/database instance as a parent to a classmethod.

```py
new_database = notion.Database.create(homepage, page_title='A new database', name_column='name')
new_page = notion.Page.create(new_database, page_title='A new database row')
```

Blocks can be created with `notion.api.blocktypefactory.BlockFactory` by appending to an exisiting Block or Page.
```py
# BlockFactory returns the new block as a Block object.
original_synced_block = notion.BlockFactory.new_synced_block(homepage)

# Adding content to the synced block
notion.BlockFactory.paragraph(original_synced_block, [prop.RichText('This is a synced block.')])

# Referencing the synced block in the new page created.
notion.BlockFactory.reference_synced_block(new_page, original_synced_block.id)
```

---
## Adding, Setting, and Deleting Page Property Values & Database Property Objects

```py
import notion.properties as prop

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

# Compound filters support combining `and`/`or` filters,
# or a single `notion.query.propfilter.PropertyFilter` can be used.

today = datetime.today().isoformat()
tomorrow = (datetime.today() + timedelta(1)).isoformat()

filter = CompoundFilter()
nested_filter = CompoundFilter()

nested_filter._or_(
        PropertyFilter.text("name", "title", "contains", "your page title"),
        PropertyFilter.text("name", "title", "contains", "your other page title"),
    )

filter._and_(
    PropertyFilter.date("date", "date", "on_or_after", today)
    PropertyFilter.date("date", "date", "before", tomorrow),
    nested_filter
)

sort = SortFilter([EntryTimestampSort.created_time_descending()])

query_params = notion.request_json(filter, sort)

query_result = new_database.query(
    payload=query_params, filter_property_values=["name", "options"]
)
```
If the list result is over 100 pages (Notions max for paginated responses), you can use a cursor included at the end to continue the query.

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
    raise NotionValidationError(args)
notion.exceptions.errors.NotionValidationError: body failed validation: body.an_incorrect_key should be not present, instead was `"value"`.
Error 400: The request body does not match the schema for the expected parameters.
```

A common error to look out for is `notion.exceptions.errors.NotionObjectNotFound`:  

This error will throw if your bot has not been added as a connection to the page.  
<img src="assets\directory_add_connections.png">  

By default, a bot will have access to the children of any Parent object it has access too.

---

More features in development, and planning to host on PyPI once a stable working version is complete.
