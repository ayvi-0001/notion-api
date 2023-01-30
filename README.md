# notion-wrapper
 
A wrapper I'm working on for Notion's API, current Notion-Version: 2022-06-28.  
This is still a work in progress, and currently has limited functionality.

Here are a few examples so far:  

---
## Pages & Properties

```py
import dotenv

import notion

# client will check .env for 'NOTION_TOKEN',
dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv())

homepage = notion.Page('773b08ff38b44521b44b115827e850f2')
homepage.last_edited.date # out: 01/15/2023
homepage.last_edited.time # out: 16:28:00

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

# For formulas and relations, use the Database endpoint 
# to pull information from the property schema.

parent_db = notion.Database(homepage.parent_id)
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
```

---
### Updating & Creating Pages/Databases
Create pages/databases using classmethods, by passing an existing page/database instance as a parent.

```py
import notion.properties as prop

new_database = notion.Database.create(parent=homepage)

expression_one = """prop("Text Column") == "Hello" ? " world!" : ''"""
expression_two = """concat(prop("Text Column"), prop("Formula"))"""

if __name__ == '__main__':
    new_database.update(
        notion.request_json(
            prop.Properties(
                prop.RichTextPropertyObject(property_name='Text Column'),
                prop.FormulaPropertyObject(expression_one, property_name='Formula'),
                prop.FormulaPropertyObject(expression_two, property_name='Message')
                )
            )
        )
```

```py
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
    notes_page = notion.Page.create(db_tasks, 
        page_title=f"Notes | {datetime.today().strftime(("%m/%d/%Y"))}")

    first_relation = notion.request_json(prop.Properties(
        prop.RelationPropertyValue([prop.NotionUUID(tasks_page.id)], 
            property_name='column related to db_tasks')))

    db_dailies.patch_properties(payload=first_relation)

    second_relation = notion.request_json(prop.Properties(
        prop.RelationPropertyValue([prop.NotionUUID(notes_page.id)], 
            property_name='column related to db_notes')))

    db_dailies.patch_properties(payload=second_relation)


if __name__ == '__main__':
    create_dailies()
```


---
### Queries

```py
import notion.query as query

query_landmarks = notion.request_json(
    query.CompoundFilter(
        query.OrOperator(
            query.PropertyFilter.text(
                'Landmark', 'rich_text', 'contains', 'Bridge', compound=True), 
        query.AndOperator(
            query.PropertyFilter.checkbox(
                'Seen', 'equals', 'false', compound=True), 
            query.PropertyFilter.number(
                'Yearly visitor count', 'greater_than', 1000000, compound=True)
            )
        )
    )
)

# out: {
#     "filter": {
#         "or": [
#             {
#                 "property": "Landmark",
#                 "rich_text": {
#                     "contains": "Bridge"
#                 }
#             },
#             {
#                 "and": [
#                     {
#                         "property": "Seen",
#                         "checkbox": {
#                             "equals": "false"
#                         }
#                     },
#                     {
#                         "property": "Yearly visitor count",
#                         "number": {
#                             "greater_than": 1000000
#                         }
#                     }
#                 ]
#             }
#         ]
#     }
# }


result = new_database.query(payload=query_landmarks).get('results')

print(result['Landmark'])
```

If the list result is over 100 pages (Notions max for paginated responses), you can use a cursor included at the end to continue the query.

---

## Exceptions & Validating Responses

```py
my_page = notion.Page('12345')
# Errors in Notion requests return an object with 'object', 'status', 'code', and 'message' keys.
# Example:
# {
#   'object': 'error', 
#   'status': 400, 
#   'code': 'validation_error', 
#   'message': 'path failed validation: path.page_id should be a valid uuid, instead was `"12345"`.'
# }
```

```sh
Traceback (most recent call last):
  File "c:\path\to\file\_.py", line 6, in <module>
    notion.Page('12345')
  File "c:\...\notion\api\notionpage.py", line 36, in __init__
    super().__init__(id, token=token, notion_version=notion_version)
  File "c:\...\notion\api\base_object.py", line 44, in __init__
    raise NotionValidationError(__failed_instance__)
notion.exceptions.errors.NotionObjectNotFound:
            <page_12345> instatiation failed validation:
            id should be a valid uuid, instead was `'12345'`

Error 404: Given the bearer token used, the resource does not exist. This error can also indicate that the resource has not been shared with owner of the bearer token.
```

```py
homepage.patch_properties(payload={'an_incorrect_key':'value'})
```

```sh
Traceback (most recent call last):
    ...
File "c:\...\notion\exceptions\validate.py", line 48, in validate_response
    raise NotionValidationError(args)
notion.exceptions.errors.NotionValidationError: body failed validation: body.an_incorrect_key should be not present, instead was `"value"`.
Error 400: The request body does not match the schema for the expected parameters.
```

A common error to look out for is `notion.exceptions.errors.NotionObjectNotFound`:  
"Error 404: Given the bearer token used, the resource does not exist. This error can also indicate that the resource has not been shared with owner of the bearer token."

This error will throw if your bot has not been added as a connection to the page.  
<img src="assets\directory_add_connections.png">  

By default, a bot will have access to the children of any Parent object it has access too.

---

<br></br>
More features in development.
