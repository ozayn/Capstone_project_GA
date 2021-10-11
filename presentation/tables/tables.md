
-----------
### Nodes Address
| name          | type    |
|:--------------|:--------|
| index         | integer |
| node_id       | integer |
| name          | number  |
| address       | string  |
| country_codes | string  |
| countries     | string  |
| sourceID      | string  |
| valid_until   | string  |
| note          | number  |
-----------
### Nodes Intermediary
| name          | type    |
|:--------------|:--------|
| index         | integer |
| node_id       | integer |
| name          | string  |
| country_codes | string  |
| countries     | string  |
| status        | number  |
| sourceID      | string  |
| valid_until   | string  |
| note          | string  |
-----------
### Nodes Officer
| name          | type    |
|:--------------|:--------|
| index         | integer |
| node_id       | integer |
| name          | string  |
| country_codes | string  |
| countries     | string  |
| sourceID      | string  |
| valid_until   | string  |
| note          | string  |
-----------
### Edges
| name        | type    |
|:------------|:--------|
| index       | integer |
| START_ID    | integer |
| TYPE        | string  |
| END_ID      | integer |
| link        | string  |
| start_date  | string  |
| end_date    | string  |
| sourceID    | string  |
| valid_until | string  |
-----------
### Nodes Entity
| name                     | type    |
|:-------------------------|:--------|
| index                    | integer |
| node_id                  | integer |
| name                     | string  |
| jurisdiction             | string  |
| jurisdiction_description | string  |
| country_codes            | string  |
| countries                | string  |
| incorporation_date       | string  |
| inactivation_date        | number  |
| struck_off_date          | number  |
| closed_date              | number  |
| ibcRUC                   | string  |
| status                   | string  |
| company_type             | string  |
| service_provider         | string  |
| sourceID                 | string  |
| valid_until              | string  |
| note                     | string  |