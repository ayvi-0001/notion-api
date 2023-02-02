# notion-wrapper
 
A wrapper I'm working on for Notion's API, current Notion-Version: 2022-06-28.  
This is still a work in progress, and currently has limited functionality.

Here are a few examples so far:  

---
## Pages & Properties

```py
import dotenv

import notion

dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv()) # client will check .env for 'NOTION_TOKEN',

homepage = notion.Page('773b08ff38b44521b44b115827e850f2')
parent_db = notion.Database(homepage.parent_id)

homepage.retrieve_property('dependencies')
# out: {
#     "dependencies": {
#         "id": "%3Fk%5EP",
#         "type": "relation",
#         "relation": [
#             {
#                 "id": "059b9e50-47c9-4d7d-80b5-4b9860f9ce9d"
#             }
#         ],
#         "has_more": false
#     }
# }

parent_db.property_schema['dependencies']
# out: {
#     "dependencies": {
#         "id": "%3Fk%5EP",
#         "name": "dependencies",
#         "type": "relation",
#         "relation": {
#             "database_id": "c2118912-7d6e-4b63-928e-f5cdf9ae53e0",
#             "type": "dual_property",
#             "dual_property": {
#                 "synced_property_name": "blocked",
#                 "synced_property_id": "ixf~"
#             }
#         }
#     }
# }

homepage.last_edited.date # out: 01/15/2023
homepage.last_edited.time # out: 16:28:00
```

---
### Updating & Creating Pages/Databases
Create pages/databases using classmethods, by passing an existing page/database instance as a parent.

```py
new_database = notion.Database.create(parent=homepage)

new_database.add_text_column('Text Column')
new_database.add_formula_column('Formula', expression="prop('Text Column') == 'Hello' ? ' world!' : ''")
new_database.add_formula_column('Message', expression="concat(prop('Text Column'), prop('Formula'))")

new_page = notion.Page.create(new_database, page_title='Page in Database')
new_page.update_text('Text Column', 'Hello')
new_database.rename_property('Message', 'Say Hello')
```
---
### Example Workflow

```py
from datetime import datetime

import notion
import notion.properties as prop

db_dailies = notion.Database('3462eb8c447640a0995d9d99de47afaa')
db_tasks = notion.Database('49f79abaf40d455fb08ee1fc2a5fdff5')
db_notes = notion.Database('d6a1e3cbc474479791d56e957d5a0416')

def create_dailies():
    daily_page = notion.Page.create(db_dailies, 
        page_title=f"Dailies | {datetime.today().strftime(("%m/%d/%Y"))}")
    tasks_page = notion.Page.create(db_tasks, 
        page_title=f"Tasks | {datetime.today().strftime(("%m/%d/%Y"))}")
    notes_page = notion.Page.create(db_notes, 
        page_title=f"Notes | {datetime.today().strftime(("%m/%d/%Y"))}")

    daily_page.set_related('Related to Tasks', [tasks_page.id])
    daily_page.set_related('Related to Notes', [notes_page.id])

    # if a multiselect option does not already exist,
    # a new one will be created.
    daily_page.set_multiselect('Tags', '...')

    daily_page.append_to_page(notion.request_json(
        prop.Children([prop.ReferenceSyncedBlockType(string_uuid_to_some_other_block)])))


if __name__ == '__main__':
    create_dailies()
```


---
### Queries

```py
import notion.query as query

query_payload = notion.request_json(
    query.CompoundFilter(
        query.AndOperator(
            query.OrOperator(
                query.PropertyFilter.text('name', 'title', 'contains', 'something'),
                query.PropertyFilter.text('name', 'title', 'contains', 'cool'),
                    ),
            query.PropertyFilter.date('date', 'date', 'on_or_after', 
                                       datetime.today().isoformat()),
            query.PropertyFilter.date('date', 'date', 'on_or_before', 
                                      (datetime.today() + timedelta(1)).isoformat()),
            query.TimestampFilter.created_time('past_week', {})
        )
    ),
    query.SortFilter([query.EntryTimestampSort.created_time_descending()])
)


query_result = new_database.query(payload=query_payload, filter_property_values=['name', 'select'])
                                                        # filter result to selected property values


# example: extract id from query results to set as relation to another page.
from jsonpath_ng.ext import parse

list_related_ids = [match.value for match in parse("$.results[*].id").find(query_result)]

new_page.set_related('related to new_database', list_related_ids)
```

If the list result is over 100 pages (Notions max for paginated responses), you can use a cursor included at the end to continue the query.

---

## Exceptions & Validating Responses

```py
# Errors in Notion requests return an object with the keys: 'object', 'status', 'code', and 'message'

homepage.patch_properties(payload={'an_incorrect_key':'value'})
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
    homepage.patch_properties(payload={'an_incorrect_key':'value'})
File "c:\...\notion\exceptions\validate.py", line 48, in validate_response
    raise NotionValidationError(args)
notion.exceptions.errors.NotionValidationError: body failed validation: body.an_incorrect_key should be not present, instead was `"value"`.
Error 400: The request body does not match the schema for the expected parameters.
```

Another common error to look out for is `notion.exceptions.errors.NotionObjectNotFound`:  

This error will throw if your bot has not been added as a connection to the page.  
<img src="assets\directory_add_connections.png">  

By default, a bot will have access to the children of any Parent object it has access too.

---

<br></br>
More features in development.
