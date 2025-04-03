## Endpoints

The root URL of this service is `https://api.ultimaker.com/connect/v1`.

GET​/

Retrieves up-time information about the API.

#### Parameters

No parameters

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The up-time information.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "ok": true,<br>    "time": "2020-08-14 09:42:15",<br>    "uptime": 1337,<br>    "version": "v1"<br>  }<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/clusters​/team_count

Counts clusters per team ID in the given list of team IDs.

#### Parameters

|Name|Description|
|---|---|
|team_ids<br><br>array[string]<br><br>(query)|List of team ids to filter on.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|Dictionary with team IDs as keys and a count of clusters as values.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "counts": {<br>      "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=": 10<br>    }<br>  }<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/clusters​/{cluster_id}

Retrieves a clusters for which the user has access to.

#### Parameters

|Name|Description|
|---|---|
|cluster_id *<br><br>string<br><br>(path)|The unique ID of the cluster to do a request for.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The registered printer cluster.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "capabilities": [<br>      "connect_with_cluster_id",<br>      "group",<br>      "print_job_action",<br>      "print_job_action_duplicate",<br>      "queue",<br>      "schedule",<br>      "status"<br>    ],<br>    "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "friendly_name": "Master-Luke",<br>    "host_guid": "5712e0ac-e90a-0344-ee91-7e8050a44c9b",<br>    "host_internal_ip": "10.183.0.34",<br>    "host_name": "ultimaker-printer-1234",<br>    "host_version": "99.99.9999-TESTING",<br>    "is_online": true,<br>    "organization_shared": false,<br>    "printer_count": 1,<br>    "printer_type": "ultimaker3",<br>    "status": "active",<br>    "team_ids": [<br>      "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>    ],<br>    "user_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>  }<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

DELETE​/clusters​/{cluster_id}

Allows the user to remove a printer cluster from their account.

#### Parameters

|Name|Description|
|---|---|
|cluster_id *<br><br>string<br><br>(path)|The unique ID of the cluster to do a request for.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|204|The cluster has been deleted.|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

POST​/clusters​/{cluster_id}​/note

Update the note of a cluster.

#### Parameters

|Name|Description|
|---|---|
|cluster_id *<br><br>string<br><br>(path)|The unique ID of the cluster to do a request for.|
|request_body *<br><br>object<br><br>(body)|The new note of a cluster.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "summary": "Example ClusterNoteUpdateRequest.",<br>    "description": "Example value for ClusterNoteUpdateRequest. May be used for generating mocks.",<br>    "value": {<br>      "note": {<br>        "note": "Hoi, ik ben Papegaai."<br>      }<br>    }<br>  }<br>}<br>```<br><br>Parameter content type<br><br>application/json|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The updated cluster.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "capabilities": [<br>      "connect_with_cluster_id",<br>      "group",<br>      "print_job_action",<br>      "print_job_action_duplicate",<br>      "queue",<br>      "schedule",<br>      "status"<br>    ],<br>    "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "friendly_name": "Master-Luke",<br>    "host_guid": "5712e0ac-e90a-0344-ee91-7e8050a44c9b",<br>    "host_internal_ip": "10.183.0.34",<br>    "host_name": "ultimaker-printer-1234",<br>    "host_version": "99.99.9999-TESTING",<br>    "is_online": true,<br>    "organization_shared": false,<br>    "printer_count": 1,<br>    "printer_type": "ultimaker3",<br>    "status": "active",<br>    "team_ids": [<br>      "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>    ],<br>    "user_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|The given data already exists.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordDuplicated",<br>      "http_status": "409",<br>      "title": "The given record already exists.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} already exists.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/clusters​/{cluster_id}​/print_jobs​/{cluster_job_id}

Returns the print job instance status and extra details about the source print job file.

#### Parameters

|Name|Description|
|---|---|
|cluster_id *<br><br>string<br><br>(path)|Unique ID of the printer cluster.|
|cluster_job_id *<br><br>string<br><br>(path)|UUID of this print job in the printer cluster. Should be used for identification purposes.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The print job details.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "assigned_to": "Master-Luke",<br>    "build_plate": {<br>      "temperature": 28,<br>      "type": "glass"<br>    },<br>    "cloud_job_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "compatible_machine_families": [<br>      "Ultimaker 3",<br>      "Ultimaker 3 Extended"<br>    ],<br>    "configuration": [<br>      {<br>        "estimated_material_volume": 2000,<br>        "extruder_index": 0,<br>        "material": {<br>          "brand": "Generic",<br>          "color": "Generic",<br>          "guid": "506c9f0d-e3aa-4bd4-b2d2-23e2425b1aa9",<br>          "material": "PLA"<br>        },<br>        "original_material_volume": 4000,<br>        "print_core_id": "BB 0.4",<br>        "temperature": 100<br>      }<br>    ],<br>    "configuration_changes_required": [<br>      {<br>        "index": 0,<br>        "is_overridable": true,<br>        "origin_id": "0fd211c3-da2e-48a3-9294-b33b753331bf",<br>        "origin_name": "White PLA",<br>        "target_id": "f624471a-2052-4dd5-ab9d-5c1e12b125cb",<br>        "target_name": "Black PLA",<br>        "type_of_change": "material_change"<br>      }<br>    ],<br>    "constraints": {<br>      "require_printer_name": "ultimakersystem-ccbdd30044ec"<br>    },<br>    "created_at": "2018-02-20T14:21:56.162Z",<br>    "force": false,<br>    "impediments_to_printing": [<br>      {<br>        "severity": "6",<br>        "translation_key": "does_not_fit_in_build_volume"<br>      }<br>    ],<br>    "is_online": true,<br>    "last_seen": 4.4,<br>    "machine_variant": "Ultimaker 3",<br>    "name": "UM3_monochromatic.gcode.gz",<br>    "network_error_count": 0,<br>    "owner": "cterbeke",<br>    "preview_url": "https://ultimaker.com/en/products/ultimaker-3",<br>    "printed_on_uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4",<br>    "printer_name": "Master-Luke",<br>    "printer_uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4",<br>    "sent_from": "cloud",<br>    "source": {<br>      "attachments": [],<br>      "content_type": "text/plain",<br>      "download_url": "https://ultimaker.com/en/products/ultimaker-3",<br>      "file_size": 5000,<br>      "job_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "job_name": "Ultimaker Robot v3.0",<br>      "library_project_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "parsing_status": "success",<br>      "status": "queued",<br>      "status_description": "The given request has been queued.",<br>      "upload_url": "https://ultimaker.com/en/products/ultimaker-3",<br>      "uploaded_at": "2017-05-26T06:44:30.420Z",<br>      "user_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "username": "user-name"<br>    },<br>    "started": true,<br>    "state": "in_progress",<br>    "status": "printing",<br>    "time_elapsed": 5356,<br>    "time_remaining": 17279,<br>    "time_total": 22635,<br>    "uuid": "fcf54df3-4ada-4302-8b72-758dabf89887"<br>  }<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

POST​/clusters​/{cluster_id}​/print_jobs​/{cluster_job_id}

Update a print job instance.

#### Parameters

|Name|Description|
|---|---|
|cluster_id *<br><br>string<br><br>(path)|Unique ID of the printer cluster.|
|cluster_job_id *<br><br>string<br><br>(path)|UUID of this print job in the printer cluster. Should be used for identification purposes.|
|request_body *<br><br>object<br><br>(body)|The print job instance update request.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "summary": "Example PrintJobInstanceUpdateRequest.",<br>    "description": "Example value for PrintJobInstanceUpdateRequest. May be used for generating mocks.",<br>    "value": {<br>      "note": "This is a large description field that can accommodate a lot of text and then some extra..."<br>    }<br>  }<br>}<br>```<br><br>Parameter content type<br><br>application/json|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The updated print job details.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "assigned_to": "Master-Luke",<br>    "build_plate": {<br>      "temperature": 28,<br>      "type": "glass"<br>    },<br>    "cloud_job_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "compatible_machine_families": [<br>      "Ultimaker 3",<br>      "Ultimaker 3 Extended"<br>    ],<br>    "configuration": [<br>      {<br>        "estimated_material_volume": 2000,<br>        "extruder_index": 0,<br>        "material": {<br>          "brand": "Generic",<br>          "color": "Generic",<br>          "guid": "506c9f0d-e3aa-4bd4-b2d2-23e2425b1aa9",<br>          "material": "PLA"<br>        },<br>        "original_material_volume": 4000,<br>        "print_core_id": "BB 0.4",<br>        "temperature": 100<br>      }<br>    ],<br>    "configuration_changes_required": [<br>      {<br>        "index": 0,<br>        "is_overridable": true,<br>        "origin_id": "0fd211c3-da2e-48a3-9294-b33b753331bf",<br>        "origin_name": "White PLA",<br>        "target_id": "f624471a-2052-4dd5-ab9d-5c1e12b125cb",<br>        "target_name": "Black PLA",<br>        "type_of_change": "material_change"<br>      }<br>    ],<br>    "constraints": {<br>      "require_printer_name": "ultimakersystem-ccbdd30044ec"<br>    },<br>    "created_at": "2018-02-20T14:21:56.162Z",<br>    "force": false,<br>    "impediments_to_printing": [<br>      {<br>        "severity": "6",<br>        "translation_key": "does_not_fit_in_build_volume"<br>      }<br>    ],<br>    "is_online": true,<br>    "last_seen": 4.4,<br>    "machine_variant": "Ultimaker 3",<br>    "name": "UM3_monochromatic.gcode.gz",<br>    "network_error_count": 0,<br>    "owner": "cterbeke",<br>    "preview_url": "https://ultimaker.com/en/products/ultimaker-3",<br>    "printed_on_uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4",<br>    "printer_name": "Master-Luke",<br>    "printer_uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4",<br>    "sent_from": "cloud",<br>    "source": {<br>      "attachments": [],<br>      "content_type": "text/plain",<br>      "download_url": "https://ultimaker.com/en/products/ultimaker-3",<br>      "file_size": 5000,<br>      "job_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "job_name": "Ultimaker Robot v3.0",<br>      "library_project_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "parsing_status": "success",<br>      "status": "queued",<br>      "status_description": "The given request has been queued.",<br>      "upload_url": "https://ultimaker.com/en/products/ultimaker-3",<br>      "uploaded_at": "2017-05-26T06:44:30.420Z",<br>      "user_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "username": "user-name"<br>    },<br>    "started": true,<br>    "state": "in_progress",<br>    "status": "printing",<br>    "time_elapsed": 5356,<br>    "time_remaining": 17279,<br>    "time_total": 22635,<br>    "uuid": "fcf54df3-4ada-4302-8b72-758dabf89887"<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|The given data already exists.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordDuplicated",<br>      "http_status": "409",<br>      "title": "The given record already exists.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} already exists.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

POST​/clusters​/{cluster_id}​/printers​/{cluster_printer_id}​/action​/{action}

Sends a printer action to the given printer's action queue.

#### Parameters

|Name|Description|
|---|---|
|action *<br><br>string<br><br>(path)|The type of a printer action.|
|cluster_id *<br><br>string<br><br>(path)|Unique ID of the printer cluster.|
|cluster_printer_id *<br><br>string<br><br>(path)|UUID of this printer in the printer cluster. Should be used for identification purposes.|
|request_body<br><br>object<br><br>(body)|The optional body parameters for printer actions.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "summary": "Example PrinterActionBodyRequest.",<br>    "description": "Example value for PrinterActionBodyRequest. May be used for generating mocks.",<br>    "value": {<br>      "name": "SuperDuperPlasticPooper"<br>    }<br>  }<br>}<br>```<br><br>Parameter content type<br><br>application/json|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|201|Indicates the action has successfully been queued.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "action_id": "5712e0ac-e90a-0344-ee91-7e8050a44c9b",<br>    "status": "pending"<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|The given data already exists.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordDuplicated",<br>      "http_status": "409",<br>      "title": "The given record already exists.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} already exists.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

POST​/clusters​/{cluster_id}​/reprint​/{original_cluster_id}​/{job_instance_uuid}

Requests the printer cluster to repeat an existing print job instance.

#### Parameters

|Name|Description|
|---|---|
|cluster_id *<br><br>string<br><br>(path)|The ID of the cluster that should print the file.|
|job_instance_uuid *<br><br>string<br><br>(path)|The ID of the print job instance that should be reprinted.|
|original_cluster_id *<br><br>string<br><br>(path)|The ID of the cluster that originally printed the file.|
|request_body<br><br>object<br><br>(body)|Parameters used when submitting a print job to the cloud for printing.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "summary": "Example PrintBodyRequest.",<br>    "description": "Example value for PrintBodyRequest. May be used for generating mocks.",<br>    "value": {<br>      "start_now": true<br>    }<br>  }<br>}<br>```<br><br>Parameter content type<br><br>application/json|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The status of your request. Note that this call adds the request to the cloud queue and and does not wait until the printer cluster has picked it up. To see the actual job status, use the cluster status call.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "job_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "job_instance_uuid": "5712e0ac-e90a-0344-ee91-7e8050a44c9b",<br>    "status": "queued"<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|This status may be returned if the cluster or printer cannot accept a new print job due to it not having a print job queue or being unavailable. It may be possible to try submitting the print job again at a later time.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "printerNotAcceptingJobs",<br>      "http_status": "409",<br>      "title": "Printer is not accepting jobs",<br>      "detail": "Printer is currently unable to accept new print jobs due to being either busy or other factors.",<br>      "meta": {<br>        "error_type": "PrinterError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

POST​/clusters​/{cluster_id}​/share

Update the sharing settings of a cluster.

#### Parameters

|Name|Description|
|---|---|
|cluster_id *<br><br>string<br><br>(path)|The unique ID of the cluster to do a request for.|
|request_body *<br><br>object<br><br>(body)|The new sharing settings.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "summary": "Example ClusterSharingUpdateRequest.",<br>    "description": "Example value for ClusterSharingUpdateRequest. May be used for generating mocks.",<br>    "value": {<br>      "organization_shared": true,<br>      "team_ids": []<br>    }<br>  }<br>}<br>```<br><br>Parameter content type<br><br>application/json|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The updated cluster.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "capabilities": [<br>      "connect_with_cluster_id",<br>      "group",<br>      "print_job_action",<br>      "print_job_action_duplicate",<br>      "queue",<br>      "schedule",<br>      "status"<br>    ],<br>    "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "friendly_name": "Master-Luke",<br>    "host_guid": "5712e0ac-e90a-0344-ee91-7e8050a44c9b",<br>    "host_internal_ip": "10.183.0.34",<br>    "host_name": "ultimaker-printer-1234",<br>    "host_version": "99.99.9999-TESTING",<br>    "is_online": true,<br>    "organization_shared": false,<br>    "printer_count": 1,<br>    "printer_type": "ultimaker3",<br>    "status": "active",<br>    "team_ids": [<br>      "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>    ],<br>    "user_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|The given data already exists.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordDuplicated",<br>      "http_status": "409",<br>      "title": "The given record already exists.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} already exists.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/clusters?

Retrieves a list of the clusters for which the user has access to.

#### Parameters

|Name|Description|
|---|---|
|limit<br><br>number<br><br>(query)|The amount of items to retrieve for pagination. 999999 default to ensure backwards compatibility.|
|machine_variant<br><br>string<br><br>(query)|The machine variant of the printer.|
|page<br><br>number<br><br>(query)|The page to get for pagination. 1 as default to ensure backwards compatibility.|
|prefer_material_1<br><br>string<br><br>(query)|Sort the clusters with a given material GUID in the first extruder.|
|prefer_material_2<br><br>string<br><br>(query)|Sort the clusters with a given material GUID in the second extruder.|
|prefer_print_core_1<br><br>string<br><br>(query)|Sort the clusters with a given print core in the first extruder.|
|prefer_print_core_2<br><br>string<br><br>(query)|Sort the clusters with a given print core in the second extruder.|
|sort<br><br>string<br><br>(query)|Sorting option for cluster queries.|
|team_ids<br><br>array[string]<br><br>(query)|Filters the clusters shared with a given team ID.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The registered printer clusters.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": [<br>    {<br>      "capabilities": [<br>        "connect_with_cluster_id",<br>        "group",<br>        "print_job_action",<br>        "print_job_action_duplicate",<br>        "queue",<br>        "schedule",<br>        "status"<br>      ],<br>      "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "friendly_name": "Master-Luke",<br>      "host_guid": "5712e0ac-e90a-0344-ee91-7e8050a44c9b",<br>      "host_internal_ip": "10.183.0.34",<br>      "host_name": "ultimaker-printer-1234",<br>      "host_version": "99.99.9999-TESTING",<br>      "is_online": true,<br>      "organization_shared": false,<br>      "printer_count": 1,<br>      "printer_type": "ultimaker3",<br>      "status": "active",<br>      "team_ids": [<br>        "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>      ],<br>      "user_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>    }<br>  ],<br>  "meta": {<br>    "limit_reached": false,<br>    "page": {<br>      "total_count": 29,<br>      "total_pages": 3<br>    }<br>  },<br>  "links": {<br>    "first": "https://example.com/items?page=1&limit=24",<br>    "last": "https://example.com/items?page=6&limit=24",<br>    "next": "https://example.com/items?page=4&limit=24",<br>    "prev": "https://example.com/items?page=2&limit=24"<br>  }<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

POST​/clusters?

Checks which of the given clusters can be accessed by the logged in user.

#### Parameters

|Name|Description|
|---|---|
|request_body *<br><br>object<br><br>(body)|The cluster IDs.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "summary": "Example ClusterIdsRequest.",<br>    "description": "Example value for ClusterIdsRequest. May be used for generating mocks.",<br>    "value": {<br>      "cluster_ids": [<br>        "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>      ]<br>    }<br>  }<br>}<br>```<br><br>Parameter content type<br><br>application/json|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The cluster IDs that can be accessed by the user.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "cluster_ids": [<br>      "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>    ]<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|The given data already exists.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordDuplicated",<br>      "http_status": "409",<br>      "title": "The given record already exists.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} already exists.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/clusters?​/{cluster_id}​/action_status​/{action_id}

Retrieves the status of an action.

#### Parameters

|Name|Description|
|---|---|
|action_id *<br><br>string<br><br>(path)|Action ID of action to be performed on printer.|
|cluster_id *<br><br>string<br><br>(path)|The unique ID of the cluster to do a request for.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The action status.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "action_id": "5712e0ac-e90a-0344-ee91-7e8050a44c9b",<br>    "status": "pending"<br>  }<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

PUT​/clusters?​/{cluster_id}​/maintenance

Adds a maintenance task to the executed maintenance for the given cluster.

#### Parameters

|Name|Description|
|---|---|
|cluster_id *<br><br>string<br><br>(path)|The unique ID of the cluster to do a request for.|
|request_body *<br><br>object<br><br>(body)|A maintenance task that has been executed.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "summary": "Example PrinterMaintenanceTaskRequest.",<br>    "description": "Example value for PrinterMaintenanceTaskRequest. May be used for generating mocks.",<br>    "value": {<br>      "task_codes": []<br>    }<br>  }<br>}<br>```<br><br>Parameter content type<br><br>application/json|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|204|The task has been added.|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|The given data already exists.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordDuplicated",<br>      "http_status": "409",<br>      "title": "The given record already exists.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} already exists.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/clusters?​/{cluster_id}​/maintenance​/completed

Retrieves a list of completed maintenance tasks.

#### Parameters

|Name|Description|
|---|---|
|cluster_id *<br><br>string<br><br>(path)|The unique ID of the cluster to do a request for.|
|limit<br><br>number<br><br>(query)|The amount of items to retrieve for pagination.|
|page<br><br>number<br><br>(query)|The page to get for pagination. 1 as default to ensure backwards compatibility.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|List of completed maintenance tasks.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": [<br>    {<br>      "completed_at": "2017-05-26T06:44:30.420Z",<br>      "task_codes": [<br>        "sline_clean_printer"<br>      ],<br>      "user_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "username": "user-name"<br>    }<br>  ],<br>  "meta": {<br>    "limit_reached": false,<br>    "page": {<br>      "total_count": 29,<br>      "total_pages": 3<br>    }<br>  },<br>  "links": {<br>    "first": "https://example.com/items?page=1&limit=24",<br>    "last": "https://example.com/items?page=6&limit=24",<br>    "next": "https://example.com/items?page=4&limit=24",<br>    "prev": "https://example.com/items?page=2&limit=24"<br>  }<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/clusters?​/{cluster_id}​/maintenance​/pending

Retrieves a list of pending maintenance tasks.

#### Parameters

|Name|Description|
|---|---|
|cluster_id *<br><br>string<br><br>(path)|The unique ID of the cluster to do a request for.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|List of pending maintenance tasks.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": [<br>    {<br>      "is_due": true,<br>      "task_rule": {<br>        "code": "um3_clean_printer",<br>        "task_details": {<br>          "type": "time_based",<br>          "value": {<br>            "interval": 7776000<br>          }<br>        }<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

POST​/clusters?​/{cluster_id}​/print​/{job_id}

Requests the printer cluster to add a print job to its queue.

#### Parameters

|Name|Description|
|---|---|
|cluster_id *<br><br>string<br><br>(path)|The secret unique ID, e.g. 'kBEeZWEifXbrXviO8mRYLx45P8k5lHVGs43XKvRniPg='.|
|job_id *<br><br>string<br><br>(path)|The secret unique ID, e.g. 'kBEeZWEifXbrXviO8mRYLx45P8k5lHVGs43XKvRniPg='.|
|request_body<br><br>object<br><br>(body)|Parameters used when submitting a print job to the cloud for printing.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "summary": "Example PrintBodyRequest.",<br>    "description": "Example value for PrintBodyRequest. May be used for generating mocks.",<br>    "value": {<br>      "start_now": true<br>    }<br>  }<br>}<br>```<br><br>Parameter content type<br><br>application/json|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The status of your request. Note that this call adds the request to the cloud queue and and does not wait until the printer cluster has picked it up. To see the actual job status, use the cluster status call.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "job_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "job_instance_uuid": "5712e0ac-e90a-0344-ee91-7e8050a44c9b",<br>    "status": "queued"<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|This status may be returned if the cluster or printer cannot accept a new print job due to it not having a print job queue or being unavailable. It may be possible to try submitting the print job again at a later time.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "printerNotAcceptingJobs",<br>      "http_status": "409",<br>      "title": "Printer is not accepting jobs",<br>      "detail": "Printer is currently unable to accept new print jobs due to being either busy or other factors.",<br>      "meta": {<br>        "error_type": "PrinterError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

POST​/clusters?​/{cluster_id}​/print_jobs​/{cluster_job_id}​/action​/{action}

Sends a printer action to the given printer job's action queue.

#### Parameters

|Name|Description|
|---|---|
|action *<br><br>string<br><br>(path)|The type of a printer action.|
|cluster_id *<br><br>string<br><br>(path)|Unique ID of the printer cluster.|
|cluster_job_id *<br><br>string<br><br>(path)|UUID of this print job in the printer cluster. Should be used for identification purposes.|
|request_body<br><br>object<br><br>(body)|The optional body parameters for print job actions.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "summary": "Example PrintJobActionBodyRequest.",<br>    "description": "Example value for PrintJobActionBodyRequest. May be used for generating mocks.",<br>    "value": {<br>      "list": "queued",<br>      "to_position": 0<br>    }<br>  }<br>}<br>```<br><br>Parameter content type<br><br>application/json|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|201|Indicates the action has successfully been queued.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "action_id": "5712e0ac-e90a-0344-ee91-7e8050a44c9b",<br>    "status": "pending"<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|The given data already exists.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordDuplicated",<br>      "http_status": "409",<br>      "title": "The given record already exists.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} already exists.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/clusters?​/{cluster_id}​/status

Retrieves the cluster status.

#### Parameters

|Name|Description|
|---|---|
|cluster_id *<br><br>string<br><br>(path)|The unique ID of the cluster to do a request for.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The printer cluster status.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "generated_time": "2017-05-26T06:44:30.420Z",<br>    "is_online": true,<br>    "print_jobs": [<br>      {<br>        "assigned_to": "Master-Luke",<br>        "build_plate": {<br>          "temperature": 28,<br>          "type": "glass"<br>        },<br>        "cloud_job_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>        "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>        "compatible_machine_families": [<br>          "Ultimaker 3",<br>          "Ultimaker 3 Extended"<br>        ],<br>        "configuration": [<br>          {<br>            "estimated_material_volume": 2000,<br>            "extruder_index": 0,<br>            "material": {<br>              "brand": "Generic",<br>              "color": "Generic",<br>              "guid": "506c9f0d-e3aa-4bd4-b2d2-23e2425b1aa9",<br>              "material": "PLA"<br>            },<br>            "original_material_volume": 4000,<br>            "print_core_id": "BB 0.4",<br>            "temperature": 100<br>          }<br>        ],<br>        "configuration_changes_required": [<br>          {<br>            "index": 0,<br>            "is_overridable": true,<br>            "origin_id": "0fd211c3-da2e-48a3-9294-b33b753331bf",<br>            "origin_name": "White PLA",<br>            "target_id": "f624471a-2052-4dd5-ab9d-5c1e12b125cb",<br>            "target_name": "Black PLA",<br>            "type_of_change": "material_change"<br>          }<br>        ],<br>        "constraints": {<br>          "require_printer_name": "ultimakersystem-ccbdd30044ec"<br>        },<br>        "created_at": "2018-02-20T14:21:56.162Z",<br>        "force": false,<br>        "impediments_to_printing": [<br>          {<br>            "severity": "6",<br>            "translation_key": "does_not_fit_in_build_volume"<br>          }<br>        ],<br>        "is_online": true,<br>        "last_seen": 4.4,<br>        "machine_variant": "Ultimaker 3",<br>        "name": "UM3_monochromatic.gcode.gz",<br>        "network_error_count": 0,<br>        "owner": "cterbeke",<br>        "preview_url": "https://ultimaker.com/en/products/ultimaker-3",<br>        "printed_on_uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4",<br>        "printer_name": "Master-Luke",<br>        "printer_uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4",<br>        "sent_from": "cloud",<br>        "started": true,<br>        "state": "in_progress",<br>        "status": "printing",<br>        "time_elapsed": 5356,<br>        "time_remaining": 17279,<br>        "time_total": 22635,<br>        "uuid": "fcf54df3-4ada-4302-8b72-758dabf89887"<br>      }<br>    ],<br>    "printers": [<br>      {<br>        "air_manager": {<br>          "filter_age": 100,<br>          "filter_max_age": 1500,<br>          "filter_status": "peak_performance",<br>          "status": "available",<br>          "supported": true<br>        },<br>        "build_plate": {<br>          "temperature": 28,<br>          "type": "glass"<br>        },<br>        "configuration": [<br>          {<br>            "estimated_material_volume": 2000,<br>            "extruder_index": 0,<br>            "material": {<br>              "brand": "Generic",<br>              "color": "Generic",<br>              "guid": "506c9f0d-e3aa-4bd4-b2d2-23e2425b1aa9",<br>              "material": "PLA"<br>            },<br>            "original_material_volume": 4000,<br>            "print_core_id": "BB 0.4",<br>            "temperature": 100<br>          }<br>        ],<br>        "enabled": true,<br>        "errors": [<br>          {<br>            "code": "AIR_MANAGER_FILTER_MISSING",<br>            "uuid": "5712e0ac-e90a-0344-ee91-7e8050a44c9b"<br>          }<br>        ],<br>        "faults": [],<br>        "firewall_enabled": true,<br>        "firmware_update_status": "up_to_date",<br>        "firmware_version": "MOD-4.2.94.20180201",<br>        "friendly_name": "Master-Luke",<br>        "ip_address": "10.183.0.119",<br>        "latest_available_firmware": "4.3.3.20180529",<br>        "machine_variant": "Ultimaker 3",<br>        "material_station": {<br>          "material_slots": [<br>            {<br>              "compatible": true,<br>              "extruder_index": 0,<br>              "material": {<br>                "brand": "Generic",<br>                "color": "Generic",<br>                "guid": "506c9f0d-e3aa-4bd4-b2d2-23e2425b1aa9",<br>                "material": "PLA"<br>              },<br>              "material_empty": false,<br>              "material_remaining": 0.5,<br>              "print_core_id": "BB 0.4",<br>              "slot_index": 0<br>            }<br>          ],<br>          "status": "available",<br>          "supported": true<br>        },<br>        "status": "idle",<br>        "unique_name": "ultimakersystem-ccbdd30044ec",<br>        "uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4"<br>      }<br>    ],<br>    "recently_completed": [<br>      {<br>        "assigned_to": "Master-Luke",<br>        "build_plate": {<br>          "temperature": 28,<br>          "type": "glass"<br>        },<br>        "cloud_job_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>        "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>        "compatible_machine_families": [<br>          "Ultimaker 3",<br>          "Ultimaker 3 Extended"<br>        ],<br>        "configuration": [<br>          {<br>            "estimated_material_volume": 2000,<br>            "extruder_index": 0,<br>            "material": {<br>              "brand": "Generic",<br>              "color": "Generic",<br>              "guid": "506c9f0d-e3aa-4bd4-b2d2-23e2425b1aa9",<br>              "material": "PLA"<br>            },<br>            "original_material_volume": 4000,<br>            "print_core_id": "BB 0.4",<br>            "temperature": 100<br>          }<br>        ],<br>        "configuration_changes_required": [<br>          {<br>            "index": 0,<br>            "is_overridable": true,<br>            "origin_id": "0fd211c3-da2e-48a3-9294-b33b753331bf",<br>            "origin_name": "White PLA",<br>            "target_id": "f624471a-2052-4dd5-ab9d-5c1e12b125cb",<br>            "target_name": "Black PLA",<br>            "type_of_change": "material_change"<br>          }<br>        ],<br>        "constraints": {<br>          "require_printer_name": "ultimakersystem-ccbdd30044ec"<br>        },<br>        "created_at": "2018-02-20T14:21:56.162Z",<br>        "deleted_at": "2018-02-20T14:22:16.235Z",<br>        "force": false,<br>        "impediments_to_printing": [<br>          {<br>            "severity": "6",<br>            "translation_key": "does_not_fit_in_build_volume"<br>          }<br>        ],<br>        "is_online": true,<br>        "last_seen": 4.4,<br>        "machine_variant": "Ultimaker 3",<br>        "name": "UM3_monochromatic.gcode.gz",<br>        "network_error_count": 0,<br>        "owner": "cterbeke",<br>        "preview_url": "https://ultimaker.com/en/products/ultimaker-3",<br>        "printed_on_uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4",<br>        "printer_name": "Master-Luke",<br>        "printer_uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4",<br>        "sent_from": "cloud",<br>        "started": true,<br>        "state": "history",<br>        "status": "finished",<br>        "time_elapsed": 5356,<br>        "time_remaining": 17279,<br>        "time_total": 22635,<br>        "uuid": "fcf54df3-4ada-4302-8b72-758dabf89887"<br>      }<br>    ]<br>  }<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

POST​/confirm-registration-pin​/{pin_code}

Confirms that the given printer cluster is allowed access with a unique pin code.

#### Parameters

|Name|Description|
|---|---|
|pin_code *<br><br>string<br><br>(path)|Pin code.|
|printer_brand<br><br>string<br><br>(query)|The brand of the printer. Defaults to ultimaker.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The printer cluster has been allowed to connect to the cloud.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "host_name": "ultimaker-printer-1234"<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|The given data already exists.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordDuplicated",<br>      "http_status": "409",<br>      "title": "The given record already exists.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} already exists.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

POST​/confirm-registration​/{connection_id}

Confirms that the given printer cluster is allowed access.

#### Parameters

|Name|Description|
|---|---|
|connection_id *<br><br>string<br><br>(path)|The unique connection ID for a printer.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The printer cluster has been allowed to connect to the cloud.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "host_name": "ultimaker-printer-1234"<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|The given data already exists.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordDuplicated",<br>      "http_status": "409",<br>      "title": "The given record already exists.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} already exists.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/filters​/print_jobs

List all available filters for print jobs

#### Parameters

No parameters

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The list of available filters.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": [<br>    {<br>      "display_name": "Material Station compatible",<br>      "key": "material_station_optimized",<br>      "type": "boolean"<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/makerbot​/printers

Retrieves a list of the printers from reflector for which the user has access to.

#### Parameters

No parameters

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The registered printer clusters.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": [<br>    {<br>      "friendly_name": "Master-Luke",<br>      "host_guid": "2857162788A9A790A1AC",<br>      "is_authorized": true,<br>      "is_online": true,<br>      "organization_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "printer_type": "lava_f",<br>      "user_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

PUT​/makerbot​/printers

Confirms that the given printer cluster is allowed access with a MakerBot account.

#### Parameters

|Name|Description|
|---|---|
|request_body *<br><br>object<br><br>(body)|The printer to confirm.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "summary": "Example ConfirmRegistrationMakerBotRequest.",<br>    "description": "Example value for ConfirmRegistrationMakerBotRequest. May be used for generating mocks.",<br>    "value": {<br>      "printer_id": "5712e0ac-e90a-0344-ee91-7e8050a44c9b"<br>    }<br>  }<br>}<br>```<br><br>Parameter content type<br><br>application/json|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The printer has been added to the account.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "host_name": "ultimaker-printer-1234"<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|The given data already exists.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordDuplicated",<br>      "http_status": "409",<br>      "title": "The given record already exists.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} already exists.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

PUT​/materials​/upload

Create a material profile object for uploading.

#### Parameters

|Name|Description|
|---|---|
|request_body *<br><br>object<br><br>(body)|The material profile upload configuration.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "summary": "Example MaterialProfileUploadRequest.",<br>    "description": "Example value for MaterialProfileUploadRequest. May be used for generating mocks.",<br>    "value": {<br>      "content_type": "application/zip",<br>      "file_size": 10000,<br>      "material_profile_name": "ultibot.umm",<br>      "origin": "https://www.ultimaker.com"<br>    }<br>  }<br>}<br>```<br><br>Parameter content type<br><br>application/json|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|201|The material profile response.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "client_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "content_type": "application/zip",<br>    "file_size": 3000,<br>    "material_profile_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "material_profile_name": "ultibot.umm",<br>    "status": "uploading",<br>    "status_description": "The given request has been queued.",<br>    "upload_url": "https://ultimaker.com/en/products/ultimaker-3",<br>    "user_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "username": "user-name"<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|The given data already exists.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordDuplicated",<br>      "http_status": "409",<br>      "title": "The given record already exists.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} already exists.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/print_jobs

Retrieves a list of print jobs for all the clusters the current user has access to.

#### Parameters

|Name|Description|
|---|---|
|cluster_ids<br><br>array[string]<br><br>(query)||
|limit<br><br>number<br><br>(query)|The amount of items to retrieve for pagination.|
|page<br><br>number<br><br>(query)|The page to get for pagination. 1 as default to ensure backwards compatibility.|
|private_only<br><br>boolean<br><br>(query)|Show only print jobs created by the current user.<br><br>--truefalse|
|search<br><br>string<br><br>(query)|Search by print job name, printer name or author name.|
|sent_from<br><br>array[string]<br><br>(query)|_Available values_ : cloud, usb, network, reprint<br><br>--cloudusbnetworkreprint|
|status<br><br>array[string]<br><br>(query)|_Available values_ : wait_approval, sending, waiting, in_progress, history, deleted<br><br>--wait_approvalsendingwaitingin_progresshistorydeleted|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|List of print jobs for accessible clusters.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": [<br>    {<br>      "assigned_to": "Master-Luke",<br>      "build_plate": {<br>        "temperature": 28,<br>        "type": "glass"<br>      },<br>      "cloud_job_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "compatible_machine_families": [<br>        "Ultimaker 3",<br>        "Ultimaker 3 Extended"<br>      ],<br>      "configuration": [<br>        {<br>          "estimated_material_volume": 2000,<br>          "extruder_index": 0,<br>          "material": {<br>            "brand": "Generic",<br>            "color": "Generic",<br>            "guid": "506c9f0d-e3aa-4bd4-b2d2-23e2425b1aa9",<br>            "material": "PLA"<br>          },<br>          "original_material_volume": 4000,<br>          "print_core_id": "BB 0.4",<br>          "temperature": 100<br>        }<br>      ],<br>      "configuration_changes_required": [<br>        {<br>          "index": 0,<br>          "is_overridable": true,<br>          "origin_id": "0fd211c3-da2e-48a3-9294-b33b753331bf",<br>          "origin_name": "White PLA",<br>          "target_id": "f624471a-2052-4dd5-ab9d-5c1e12b125cb",<br>          "target_name": "Black PLA",<br>          "type_of_change": "material_change"<br>        }<br>      ],<br>      "constraints": {<br>        "require_printer_name": "ultimakersystem-ccbdd30044ec"<br>      },<br>      "created_at": "2018-02-20T14:21:56.162Z",<br>      "force": false,<br>      "impediments_to_printing": [<br>        {<br>          "severity": "6",<br>          "translation_key": "does_not_fit_in_build_volume"<br>        }<br>      ],<br>      "is_online": true,<br>      "last_seen": 4.4,<br>      "machine_variant": "Ultimaker 3",<br>      "name": "UM3_monochromatic.gcode.gz",<br>      "network_error_count": 0,<br>      "owner": "cterbeke",<br>      "preview_url": "https://ultimaker.com/en/products/ultimaker-3",<br>      "printed_on_uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4",<br>      "printer_name": "Master-Luke",<br>      "printer_uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4",<br>      "sent_from": "cloud",<br>      "started": true,<br>      "state": "in_progress",<br>      "status": "printing",<br>      "time_elapsed": 5356,<br>      "time_remaining": 17279,<br>      "time_total": 22635,<br>      "uuid": "fcf54df3-4ada-4302-8b72-758dabf89887"<br>    }<br>  ],<br>  "meta": {<br>    "limit_reached": false,<br>    "page": {<br>      "total_count": 29,<br>      "total_pages": 3<br>    }<br>  },<br>  "links": {<br>    "first": "https://example.com/items?page=1&limit=24",<br>    "last": "https://example.com/items?page=6&limit=24",<br>    "next": "https://example.com/items?page=4&limit=24",<br>    "prev": "https://example.com/items?page=2&limit=24"<br>  }<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/print_jobs​/reports

Get print job instances.

#### Parameters

|Name|Description|
|---|---|
|cluster_ids<br><br>array[string]<br><br>(query)||
|end_date *<br><br>string<br><br>(path)|The end date of the print job instances. Upper limit of the time range.|
|limit<br><br>number<br><br>(query)|The amount of items to retrieve for pagination. 999999 default to ensure backwards compatibility.|
|page<br><br>number<br><br>(query)|The page to get for pagination. 1 as default to ensure backwards compatibility.|
|start_date *<br><br>string<br><br>(path)|The start time of the print job instance. Lower limit of the time range.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The print job instances were successfully retrieved.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": [<br>    {<br>      "assigned_to": "Master-Luke",<br>      "build_plate": {<br>        "temperature": 28,<br>        "type": "glass"<br>      },<br>      "cloud_job_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>      "compatible_machine_families": [<br>        "Ultimaker 3",<br>        "Ultimaker 3 Extended"<br>      ],<br>      "configuration": [<br>        {<br>          "estimated_material_volume": 2000,<br>          "extruder_index": 0,<br>          "material": {<br>            "brand": "Generic",<br>            "color": "Generic",<br>            "guid": "506c9f0d-e3aa-4bd4-b2d2-23e2425b1aa9",<br>            "material": "PLA"<br>          },<br>          "original_material_volume": 4000,<br>          "print_core_id": "BB 0.4",<br>          "temperature": 100<br>        }<br>      ],<br>      "configuration_changes_required": [<br>        {<br>          "index": 0,<br>          "origin_id": "0fd211c3-da2e-48a3-9294-b33b753331bf",<br>          "origin_name": "White PLA",<br>          "target_id": "f624471a-2052-4dd5-ab9d-5c1e12b125cb",<br>          "target_name": "Black PLA",<br>          "type_of_change": "material_change"<br>        }<br>      ],<br>      "constraints": {<br>        "require_printer_name": "ultimakersystem-ccbdd30044ec"<br>      },<br>      "created_at": "2018-02-20T14:21:56.162Z",<br>      "force": false,<br>      "impediments_to_printing": [<br>        {<br>          "severity": "6",<br>          "translation_key": "does_not_fit_in_build_volume"<br>        }<br>      ],<br>      "last_seen": 4.4,<br>      "machine_variant": "Ultimaker 3",<br>      "name": "UM3_monochromatic.gcode.gz",<br>      "network_error_count": 0,<br>      "owner": "cterbeke",<br>      "printed_on_uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4",<br>      "printer_name": "Master-Luke",<br>      "printer_uuid": "005aaa91-31a0-4a53-96bb-0cf446e48ff4",<br>      "sent_from": "cloud",<br>      "started": true,<br>      "state": "in_progress",<br>      "status": "printing",<br>      "time_elapsed": 5356,<br>      "time_total": 22635,<br>      "uuid": "fcf54df3-4ada-4302-8b72-758dabf89887"<br>    }<br>  ],<br>  "meta": {<br>    "limit_reached": false,<br>    "page": {<br>      "total_count": 29,<br>      "total_pages": 3<br>    }<br>  },<br>  "links": {<br>    "first": "https://example.com/items?page=1&limit=24",<br>    "last": "https://example.com/items?page=6&limit=24",<br>    "next": "https://example.com/items?page=4&limit=24",<br>    "prev": "https://example.com/items?page=2&limit=24"<br>  }<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/settings

Get the current organization settings.

#### Parameters

No parameters

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|A Dictionary with the organization settings.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "enable_print_prep": false,<br>    "require_print_approval": false<br>  }<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

POST​/settings

Update the current organization settings.

#### Parameters

|Name|Description|
|---|---|
|request_body *<br><br>object<br><br>(body)|A Dictionary with the organization settings.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "summary": "Example OrganizationSettings.",<br>    "description": "Example value for OrganizationSettings. May be used for generating mocks.",<br>    "value": {<br>      "enable_print_prep": false,<br>      "require_print_approval": false<br>    }<br>  }<br>}<br>```<br><br>Parameter content type<br><br>application/json|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|A Dictionary with the organization settings.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "enable_print_prep": false,<br>    "require_print_approval": false<br>  }<br>}<br>```|
|400|The given data could not be validated.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "requiredField",<br>      "http_status": "400",<br>      "title": "A required field is missing.",<br>      "meta": {<br>        "translatable": "%{field_name} is required.",<br>        "model_name": "ExampleRequest",<br>        "field_name": "field_name",<br>        "error_type": "ModelValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|409|The given data already exists.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordDuplicated",<br>      "http_status": "409",<br>      "title": "The given record already exists.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} already exists.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/spec

Retrieves the OpenAPI specification for the API.

#### Parameters

|Name|Description|
|---|---|
|version<br><br>string<br><br>(query)|The OpenAPI version. Defaults to the lowest available version.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|The OpenAPI specification.|
|400|The requested OpenAPI version is not supported.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "openApiVersionNotSupported",<br>      "http_status": "404",<br>      "title": "The given OpenAPI version is not supported.",<br>      "meta": {<br>        "given_value": "1.0.0",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

DELETE​/teams​/{team_id}

Removes the given team from all resources in the database.

#### Parameters

|Name|Description|
|---|---|
|team_id *<br><br>string<br><br>(path)|The unique ID of the team.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|204|The team has been removed from all applicable resources.|
|401|The authentication header was not given.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "noBearerToken",<br>      "http_status": "401",<br>      "title": "No bearer token has been given to authenticate the request.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|403|The authentication has expired.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "tokenExpired",<br>      "http_status": "403",<br>      "title": "The given token has expired.",<br>      "meta": {<br>        "error_type": "AuthError"<br>      }<br>    }<br>  ]<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/teapot

Requests for brewing coffee.

#### Parameters

No parameters

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|204|The server accepts the coffee brewing request.|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|418|The server refuses to brew coffee because it is, permanently, a teapot.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "iAmATeapot",<br>      "http_status": "418",<br>      "title": "The server refuses to brew coffee because it is, permanently, a teapot.",<br>      "meta": {<br>        "error_type": "TeapotError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

GET​/user​/{user_id}​/clusters

Retrieves the clusters for user and organizations

#### Parameters

|Name|Description|
|---|---|
|organization_ids<br><br>array[string]<br><br>(query)|The organization ids for search.|
|user_id *<br><br>string<br><br>(path)|The unique ID of the user.|

#### Responses

Response content type

application/json

|Code|Description|
|---|---|
|200|List of clusters<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "data": {<br>    "capabilities": [<br>      "connect_with_cluster_id",<br>      "group",<br>      "print_job_action",<br>      "print_job_action_duplicate",<br>      "queue",<br>      "schedule",<br>      "status"<br>    ],<br>    "cluster_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE=",<br>    "friendly_name": "Master-Luke",<br>    "host_guid": "5712e0ac-e90a-0344-ee91-7e8050a44c9b",<br>    "host_internal_ip": "10.183.0.34",<br>    "host_name": "ultimaker-printer-1234",<br>    "host_version": "99.99.9999-TESTING",<br>    "is_online": true,<br>    "organization_shared": false,<br>    "printer_count": 1,<br>    "printer_type": "ultimaker3",<br>    "status": "active",<br>    "team_ids": [<br>      "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>    ],<br>    "user_id": "ABCDefGHIjKlMNOpQrSTUvYxWZ0-1234567890abcDE="<br>  }<br>}<br>```|
|404|The requested resource could not be found.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "recordNotFound",<br>      "http_status": "404",<br>      "title": "The given record does not exist.",<br>      "meta": {<br>        "record_name": "record_name",<br>        "translatable": "The given %{record_name} does not exist.",<br>        "error_type": "ValidationError"<br>      }<br>    }<br>  ]<br>}<br>```|
|500|An unexpected error occurred.<br><br>- Example Value<br>- Model<br><br>```<br>{<br>  "errors": [<br>    {<br>      "id": "00000000-1111-2222-3333-444444444444",<br>      "code": "unexpectedError",<br>      "http_status": "500",<br>      "title": "An unexpected error has occurred.",<br>      "meta": {<br>        "error_type": "ProgrammingError"<br>      }<br>    }<br>  ]<br>}<br>```|

#### Models

ActionStatusResponse{|   |   |
|---|---|
|description:|Response model for the status of print/printer/print job actions.|
|action_id*|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>Action ID of action to be performed on printer.|
|status*|string<br><br>The status of the print job action.<br><br>Enum:  <br>Array [ 5 ]|
|status_details|Union type not supported in OpenAPI v2. See x-oneOf property or use OpenAPI v3.{...}|
|| }

ApiUptimeResponse{|   |   |
|---|---|
|description:|A response model for the API update endpoint.|
|ok*|boolean<br><br>Whether all dependencies can be reached.|
|time*|string<br><br>The current date/time in UTC.|
|uptime*|number<br><br>Amount of seconds since the server was started.|
|version*|string<br><br>The API version number.|
|| }

AttachmentResponse{|   |   |
|---|---|
|description:|Represents a file attachment.|
|content_type*|string  <br>pattern: /^(application\|audio\|image\|message\|multipart\|text\|video\|x-token\|model)\/([^\s]+)$/<br><br>The content type of the attachment.|
|download_url*|string  <br>pattern: /^[a-z]+:\/\/[^\s/$.?#].[^\s]*$/<br><br>A signed URL to download the file.|
|file_name*|string  <br>maxLength: 255  <br>minLength: 3  <br>pattern: /^(?!(?:COM[0-9]\|CON\|LPT[0-9]\|NUL\|PRN\|AUX\|com[0-9]\|con\|lpt[0-9]\|nul\|prn\|aux)\|\s\|[\.]{2,})[^\\\/:*\"?<>\|]{1,}\.[a-zA-Z0-9]+$/<br><br>The name of the file.|
|| }

ClusterIdsRequest{|   |   |
|---|---|
|description:|Model for requests to fetch a list of cluster IDs.|
|cluster_ids|[...]|
|| }

ClusterIdsResponse{|   |   |
|---|---|
|description:|Model for responses to return a list of cluster IDs.|
|cluster_ids|[...]|
|| }

ClusterNote{|   |   |
|---|---|
|description:|Model for the note of a cluster.|
|note*|string  <br>maxLength: 3500  <br>minLength: 1<br><br>The large description of the item.|
|| }

ClusterNoteUpdateRequest{|   |   |
|---|---|
|description:|Model with parameters for updating the note of a cluster.|
|note|ClusterNote{...}|
|| }

ClusterPrintCoreConfiguration{|   |   |
|---|---|
|description:|Model for the status of a configuration object in a cluster printer.|
|estimated_material_volume|number<br><br>The amount in mm3 of filament remaining in the filament bay before the print started.|
|extruder_index*|number<br><br>The position of the extruder on the machine as list index. Numbered from left to right.|
|material|ClusterPrinterConfigurationMaterial{...}|
|original_material_volume|number<br><br>The original amount in mm3 of filament in the filament bay.|
|print_core_id|string<br><br>The type of print core inserted at this position, e.g. 'AA 0.4'.|
|temperature|number($float)<br><br>The current temperature of print core, degrees celsius|
|| }

ClusterPrintJobConfigurationChange{|   |   |
|---|---|
|description:|Model for the types of changes that are needed before a print job can start|
|index|number<br><br>The hotend slot or extruder index to change|
|origin_id*|string<br><br>Original/current material guid or hotend id|
|origin_name|string<br><br>Original/current material name or hotend id|
|target_id*|string<br><br>Target material guid or hotend id|
|target_name|string<br><br>Target material name or hotend id|
|type_of_change|string<br><br>The type of configuration change.<br><br>Enum:  <br>Array [ 4 ]|
|| }

ClusterPrintJobConstraints{|   |   |
|---|---|
|description:|Model for holding print job constraints as sub-model for ClusterPrintJobStatus.constraints.|
|require_printer_name|string<br><br>Unique name of the printer that this job should be printed on.Should be one of the unique_name field values in the cluster, e.g. 'ultimakersystem-ccbdd30044ec'|
|| }

ClusterPrintJobImpediment{|   |   |
|---|---|
|description:|Model for the reasons that prevent this job from being printed on the associated printer|
|severity*|string<br><br>A number indicating the severity of the problem, with higher being more severe|
|translation_key*|string<br><br>A string indicating a reason the print cannot be printed, such as 'does_not_fit_in_build_volume'|
|| }

ClusterPrinterAirManager{|   |   |
|---|---|
|description:|Model for the status of the Air Manager that could be installed on the printer.|
|filter_age|number<br><br>The amount of hours the Air Manager filter has been in use.|
|filter_max_age|number<br><br>The maximum amount of hours the Air Manager filter should be used before replacing it.|
|filter_status|string<br><br>The status of the Air Manager filter.<br><br>Enum:  <br>Array [ 5 ]|
|status|string<br><br>The status of the Air Manager.<br><br>Enum:  <br>Array [ 4 ]|
|supported*|boolean<br><br>Whether this printer supports the Air Manager or not.|
|| }

ClusterPrinterBuildPlate{|   |   |
|---|---|
|description:|Model for the status of a configuration object in a cluster printer.|
|temperature|number($float)<br><br>The current temperature of build plate, degrees celsius|
|type|string<br><br>The type of build plate<br><br>Enum:  <br>Array [ 4 ]|
|| }

ClusterPrinterChamber{|   |   |
|---|---|
|description:|Model for chamber in cluster printer.|
|temperature|number<br><br>The current temperature of chamber, degrees celsius|
|| }

ClusterPrinterConfigurationMaterial{|   |   |
|---|---|
|description:|Model for the material of a configuration object in a cluster printer.|
|brand|string<br><br>The brand of material in this print core, e.g. 'Ultimaker'.|
|color|string<br><br>The color of material in this print core, e.g. 'Blue'.|
|guid|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>The GUID of the material in this print core, e.g. '506c9f0d-e3aa-4bd4-b2d2-23e2425b1aa9'.|
|material|string<br><br>The type of material in this print core, e.g. 'PLA'.|
|| }

ClusterPrinterError{|   |   |
|---|---|
|description:|Model for an error that is currently happening on the printer.|
|code*|string<br><br>The error code.|
|uuid*|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>The unique error ID for traceability.|
|| }

ClusterPrinterFault{|   |   |
|---|---|
|description:|Model for a fault from the Marvin service from a printer.|
|code*|string<br><br>A short "error code" which identifies this kind of warning.|
|data|{...}|
|message*|string<br><br>Human readable description of the warning. This is intended for developer eyes.|
|severity*|string<br><br>The severity of a printer fault.<br><br>Enum:  <br>Array [ 9 ]|
|timestamp*|string<br><br>The date and time when this warning was created in ISO 8601.|
|uuid*|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>UUID to identify this warning instance.|
|| }

ClusterPrinterMaterialStation{|   |   |
|---|---|
|description:|Model for the status of the Material Station that could be installed on the printer.|
|material_slots|[...]|
|status|string<br><br>The status of the Material Station.<br><br>Enum:  <br>Array [ 4 ]|
|supported*|boolean<br><br>Whether this printer supports the Material Station or not.|
|| }

ClusterPrinterMaterialStationSlot{|   |   |
|---|---|
|description:|Data about a slot in the Material Station.|
|compatible*|boolean<br><br>Whether the loaded material is compatible with the print core that it is loaded towards.|
|extruder_index*|number<br><br>The position of the extruder on the machine as list index. Numbered from left to right.|
|material|ClusterPrinterConfigurationMaterial{...}|
|material_empty|boolean<br><br>Is true if no more filament is available|
|material_remaining*|number($float)  <br>maximum: 1  <br>minimum: -1<br><br>Estimation of how much material is remaining on a spool. Value between 0 and 1, or -1 when missing.|
|print_core_id|string<br><br>The type of print core inserted at this position, e.g. 'AA 0.4'.|
|slot_index*|number  <br>maximum: 5  <br>minimum: 0<br><br>The index of the slot in the station from left to right. Labelled A to F on the product.|
|| }

ClusterPrinterStatus{|   |   |
|---|---|
|description:|Model for the status of a single printer in a cluster.|
|air_manager|ClusterPrinterAirManager{...}|
|build_plate|ClusterPrinterBuildPlate{...}|
|chamber|ClusterPrinterChamber{...}|
|configuration|[...]|
|enabled*|boolean<br><br>A printer can be disabled if it should not receive new jobs. By default every printer is enabled.|
|errors|[...]|
|faults|[...]|
|firewall_enabled|boolean<br><br>Whether or not the firewall is enabled for this printer.|
|firmware_channel|string<br><br>The configured channel to put firmware updates from.<br><br>Enum:  <br>Array [ 3 ]|
|firmware_update_status|string<br><br>Whether the printer's firmware is up-to-date.<br><br>Enum:  <br>Array [ 6 ]|
|firmware_version|string  <br>maxLength: 64  <br>minLength: 3<br><br>Firmware version installed on the printer. Can be different for all printers in a cluster.|
|friendly_name*|string<br><br>Human readable name of the printer. Can be used for identification purposes.|
|ip_address|string<br><br>The IP address of the printer in the local network.|
|latest_available_firmware|string<br><br>The version of the latest firmware that is available|
|machine_variant*|string<br><br>The type of printer. Can be 'Ultimaker 3' or 'Ultimaker 3 Extended'.<br><br>Enum:  <br>Array [ 10 ]|
|maintenance_required|boolean<br><br>Indicated if maintenance is necessary|
|material_station|ClusterPrinterMaterialStation{...}|
|pin_code_lock_enabled|boolean<br><br>Whether or not the pin code lock is enabled for this printer.|
|reserved_by|string<br><br>A printer can be claimed by a specific print job.|
|status*|string<br><br>The status of the printer.<br><br>Enum:  <br>Array [ 7 ]|
|status_detail|string<br><br>Extra detail about the status of the printer.<br><br>Enum:  <br>Array [ 13 ]|
|unique_name*|string<br><br>The unique name of the printer in the network.|
|uuid*|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>The unique ID of the printer, also known as GUID. Empty Guid for MakerBot printers.|
|| }

ClusterResponse{|   |   |
|---|---|
|description:|Model for the list of clusters sent to the users.|
|capabilities|[...]|
|cluster_id*|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The secret unique ID, e.g. 'kBEeZWEifXbrXviO8mRYLx45P8k5lHVGs43XKvRniPg='.|
|display_status|string<br><br>The status of the printer that is used for display purpose.<br><br>Enum:  <br>Array [ 29 ]|
|friendly_name*|string<br><br>Human readable name of the host. Can be used for identification purposes.|
|host_current_print_job|PrintJobInstanceResponse{...}|
|host_guid*|string  <br>maxLength: 36  <br>minLength: 20  <br>pattern: /^(^[0-9A-F]{20}$)\|\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>The unique identifier of the printer that never changes.|
|host_internal_ip|string<br><br>The IP address of the printer in the local network.|
|host_name*|string  <br>maxLength: 64  <br>minLength: 3<br><br>The name of the printer as configured during the Wi-Fi setup. Used as identifier for end users.|
|host_print_job_count|number  <br>maximum: 9223372036854776000  <br>minimum: -9223372036854776000<br><br>The number of print jobs printing or waiting.|
|host_printer|ClusterPrinterStatus{...}|
|host_remaining_print_time|number  <br>maximum: 9223372036854776000  <br>minimum: -9223372036854776000<br><br>The total estimated printing time for all jobs in seconds.|
|host_version|string  <br>maxLength: 64  <br>minLength: 3<br><br>The firmware version of the cluster host. This is where the Stardust client is running on.|
|is_online|boolean<br><br>Whether this cluster is currently connected to the cloud.|
|maintenance_due|boolean<br><br>Whether the printer has at least one due maintenance task.|
|note|ClusterNote{...}|
|organization_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The ID of an organization the cluster might be associated with. Note: In the context of the API, the term "organization" can be read as meaning "workspace".|
|organization_shared|boolean  <br>default: false<br><br>Designates whether the cluster is shared with the entire organization.|
|printer_count*|number<br><br>The amount of printers connected to the cluster.|
|printer_type|string<br><br>The type of printer.<br><br>Enum:  <br>Array [ 19 ]|
|status*|string  <br>default: active<br><br>The status of the cluster authentication.<br><br>Enum:  <br>Array [ 2 ]|
|team_ids|[...]|
|user_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The ID of the user that authenticated this cluster.|
|| }

ClusterSharingUpdateRequest{|   |   |
|---|---|
|description:|Model with parameters for updating cluster sharing settings.  <br>TODO: in the future we can add organization sharing via this model as well.|
|organization_shared|boolean  <br>default: false<br><br>Designates whether the cluster is shared with the entire organization.This field must be left empty or set to 'False' when using 'team_ids'.|
|team_ids|[...]|
|| }

ClusterStatusResponse{|   |   |
|---|---|
|description:|Model for the responses we exchange from the printer clusters to the gateway for the cluster status.|
|generated_time|string($date-time)<br><br>The datetime when the object was generated on the server-side.|
|is_online|boolean<br><br>Whether the cluster is online.|
|print_jobs|[...]|
|printers|[...]|
|recently_completed|[...]|
|| }

ClusterTeamCountResponse{|   |   |
|---|---|
|description:|Request for the number of clusters.|
|counts|{...}|
|| }

ConfirmRegistrationMakerBotRequest{|   |   |
|---|---|
|description:|Model for confirming the registration of a MakerBot printer.|
|printer_id*|string  <br>maxLength: 36  <br>minLength: 20  <br>pattern: /^(^[0-9A-F]{20}$)\|\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>The unique identifier of the printer that never changes.|
|| }

ErrorObject{|   |   |
|---|---|
|description:|Model for the error responses according to the JSON-API standard.|
|code*|string<br><br>An application-specific error code, expressed as a string value.<br><br>Enum:  <br>Array [ 109 ]|
|detail|string<br><br>A human-readable explanation specific to this occurrence of the problem. Like title, this field's value can be localized.|
|http_status*|string<br><br>The HTTP status code applicable to this problem, converted to string.|
|id*|string<br><br>Unique identifier for this particular occurrence of the problem.|
|meta|{...}|
|title*|string<br><br>A short, human-readable summary of the problem that SHOULD NOT change from occurrence to occurrence of the problem, except for purposes of localization.|
|| }

FilterOption{|   |   |
|---|---|
|description:|Model for an option in the filter.|
|display_name|string<br><br>The display name of the option.|
|key*|string<br><br>The key of the option.|
|| }

FilterResponse{|   |   |
|---|---|
|description:|Response model for the available filters.|
|display_name*|string<br><br>The display name of the filter.|
|key*|string<br><br>The key of the filter.|
|options|[...]|
|type*|string<br><br>The type of the filters.<br><br>Enum:  <br>Array [ 4 ]|
|| }

MakerBotPrinterResponse{|   |   |
|---|---|
|description:|Model for the list of authorized MakerBot printers response.|
|friendly_name*|string<br><br>Human readable name of the printer. Can be used for identification purposes.|
|host_guid*|string  <br>maxLength: 36  <br>minLength: 20  <br>pattern: /^(^[0-9A-F]{20}$)\|\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>The unique identifier of the printer that never changes.|
|is_authorized*|boolean<br><br>Defines if the user is already authorized to this printer in Digital Factory|
|is_online*|boolean<br><br>Whether the printer is currently online or not.|
|organization_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The printer's organization, if any.|
|printer_type*|string<br><br>The type of printer.<br><br>Enum:  <br>Array [ 9 ]|
|user_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The ID of the user who added this printer, if any.|
|| }

MaterialProfileResponse{|   |   |
|---|---|
|description:|Model for response of the material profile object.|
|client_id*|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The ID of the OAuth2 client that uploaded this profile.|
|content_type*|string  <br>pattern: /^(application\|audio\|image\|message\|multipart\|text\|video\|x-token\|model)\/([^\s]+)$/<br><br>The content type of the item.|
|file_size|number  <br>maximum: 1073741824  <br>minimum: 0<br><br>The size of the uploaded file.|
|material_profile_id*|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The ID of the material profile package.|
|material_profile_name*|string<br><br>The name of the material profile package file.|
|status*|string<br><br>The uploading status of the file.<br><br>Enum:  <br>Array [ 3 ]|
|status_description|string<br><br>Contains more details about the status, e.g. the cause of failures.|
|upload_url|string  <br>pattern: /^[a-z]+:\/\/[^\s/$.?#].[^\s]*$/<br><br>The one-time use URL where the file must be uploaded to (only if status is uploading).|
|user_id*|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The ID of the user that uploaded this profile.|
|username*|string  <br>maxLength: 100  <br>minLength: 3  <br>pattern: /^[A-Za-z0-9]+(?:[ _.-][A-Za-z0-9]+)*$/  <br>x-pattern-error: usernameInvalid<br><br>The user's unique username.|
|| }

MaterialProfileUploadRequest{|   |   |
|---|---|
|description:|Model for requests to upload a material profiles package file.|
|content_type*|string  <br>pattern: /^(application\|audio\|image\|message\|multipart\|text\|video\|x-token\|model)\/([^\s]+)$/<br><br>The content type of the item.|
|file_size*|number  <br>maximum: 1073741824  <br>minimum: 1<br><br>The size of the file in bytes.|
|material_profile_name*|string  <br>maxLength: 255  <br>minLength: 3  <br>pattern: /^(?!(?:COM[0-9]\|CON\|LPT[0-9]\|NUL\|PRN\|AUX\|com[0-9]\|con\|lpt[0-9]\|nul\|prn\|aux)\|\s\|[\.]{2,})[^\\\/:*\"?<>\|]{1,}\.[a-zA-Z0-9]+$/<br><br>The file name of the material profile package, including the file extension.|
|origin*|string<br><br>The origin of the client that will upload the print job to storage.Used to verify the upload occurs from the same location as the request.|
|| }

OrganizationSettings{|   |   |
|---|---|
|description:|Model for organization specific settings.|
|enable_print_prep|boolean<br><br>Enables print prep for the workspace even if no makerbot printers were imported.|
|require_print_approval|boolean<br><br>Whether or not print jobs require approval before they can be printed.|
|| }

PaginationLinks{|   |   |
|---|---|
|description:|Model for links used for pagination.|
|first|string  <br>pattern: /^[a-z]+:\/\/[^\s/$.?#].[^\s]*$/<br><br>The URL for the first page.|
|last|string  <br>pattern: /^[a-z]+:\/\/[^\s/$.?#].[^\s]*$/<br><br>The URL for the last page.|
|next|string  <br>pattern: /^[a-z]+:\/\/[^\s/$.?#].[^\s]*$/<br><br>The URL for the next page.|
|prev|string  <br>pattern: /^[a-z]+:\/\/[^\s/$.?#].[^\s]*$/<br><br>The URL for the previous page.|
|| }

PaginationMetadata{|   |   |
|---|---|
|description:|Model for the metadata used for pagination.|
|total_count|number<br><br>The total count of items.|
|total_pages|number<br><br>The total number of pages when pagination is applied.|
|| }

PrintBodyRequest{|   |   |
|---|---|
|description:|Parameters used when submitting a print job to the cloud for printing.|
|start_now|boolean  <br>default: true<br><br>Whether to start the print job now. When false, the print job will be added to the cloud queue.|
|| }

PrintJobActionBodyRequest{|   |   |
|---|---|
|description:|Model holding the body arguments for a print job action.  <br>This contains all possible fields from PrintJobActionRequest.action_details, as the API receives any in the  <br>message body.|
|list|string<br><br>On action 'move', move the print job to this list in the cluster.|
|message|string  <br>maxLength: 1000<br><br>The approval/rejection message to be sent to the user.|
|quantity|number<br><br>On action 'abort' or 'duplicate', specify a quantity of jobs to abort or duplicate.|
|to_position|number  <br>minimum: 0<br><br>On action 'move', move the print job to this position in the cluster.|
|| }

PrintJobBuildPlateMetadata{|   |   |
|---|---|
|description:|The metadata model for the build plate of the print job.|
|initial_temperature|number($float)<br><br>The temperature the build plate needs to be at the start of the print.|
|temperature|number($float)<br><br>The current temperature of build plate, degrees celsius|
|type|string<br><br>The type of build plate<br><br>Enum:  <br>Array [ 4 ]|
|| }

PrintJobBuildVolumeMetadata{|   |   |
|---|---|
|description:|The metadata model for the build volume of the print job.|
|temperature|number($float)<br><br>The desired temperature of the build volume at the start of the print.|
|| }

PrintJobCoordinatesMetadata{|   |   |
|---|---|
|description:|The metadata model for print volume coordinates.|
|x|number($float)<br><br>The X coordinate of the print volume.|
|y|number($float)<br><br>The Y coordinate of the print volume.|
|z|number($float)<br><br>The Z coordinate of the print volume.|
|| }

PrintJobDetailsResponse{|   |   |
|---|---|
|description:|Data returned in the Connect API print job instance details endpoint,  <br>which also includes details about the original print job file.|
|assigned_to|string<br><br>The name of the printer this job is assigned to while being queued.|
|build_plate|ClusterPrinterBuildPlate{...}|
|cloud_job_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>Unique cloud ID of a print job if it originated in the cloud.It may be empty in case the user does not have access to the print job.|
|cluster_id*|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The unique cloud cluster ID of the printer this job is assigned to.|
|compatible_machine_families|[...]|
|configuration|[...]|
|configuration_changes_required|[...]|
|constraints|ClusterPrintJobConstraints{...}|
|created_at*|string($date-time)<br><br>The timestamp when the job was created in Cura Connect.|
|deleted_at|string($date-time)<br><br>The time when this print job was deleted.|
|force*|boolean<br><br>Allow this job to be printed despite of mismatching configurations.|
|impediments_to_printing|[...]|
|is_online*|boolean<br><br>Whether the cluster is currently connected to the cloud.|
|last_seen|number($float)<br><br>The number of seconds since this job was checked.|
|machine_variant*|string<br><br>The machine type that this job should be printed on.Coincides with the machine_type field of the printer object.<br><br>Enum:  <br>Array [ 10 ]|
|name*|string<br><br>The name of the print job. Usually the name of the .gcode file.|
|network_error_count|number<br><br>The number of errors encountered when requesting data for this print job.|
|note|string  <br>maxLength: 500<br><br>A note for the print job instance.|
|owner|string<br><br>The name of the user who added the print job to Cura Connect.|
|owner_deleted|boolean<br><br>Set to true if the user who started the print job has been deleted.|
|owner_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The unique ID of the user who started the print job.|
|preview_url|string  <br>pattern: /^[a-z]+:\/\/[^\s/$.?#].[^\s]*$/<br><br>The URL where to download a preview image from for this print job.|
|printed_on_uuid|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>UUID of the printer used to print this job.|
|printer_name|string<br><br>The human readable name of the printer this job is assigned to.|
|printer_uuid|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>UUID of the printer that the job is currently printing on or assigned to.|
|sent_from*|string<br><br>The type of client that sent the print job to the printer.<br><br>Enum:  <br>Array [ 4 ]|
|source|PrintJobResponse{...}|
|started*|boolean<br><br>Whether the job has started printing or not.|
|state*|string  <br>default: in_progress<br><br>The status of print jobs. Can be one of - in_progress, waiting, history.<br><br>Enum:  <br>Array [ 6 ]|
|status*|string<br><br>The status of the print job.<br><br>Enum:  <br>Array [ 28 ]|
|status_detail|string<br><br>Gives more detail about the status of the print job.<br><br>Enum:  <br>Array [ 9 ]|
|status_message|UserMessage{...}|
|time_elapsed|number<br><br>The remaining printing time in seconds.|
|time_remaining*|number<br><br>The amount of time seconds remaining for printing, in seconds. For waiting jobs, includes time before starting.|
|time_total*|number<br><br>The total printing time in seconds.|
|uuid*|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>UUID of this print job. Should be used for identification purposes.|
|| }

PrintJobExtruderMetadata{|   |   |
|---|---|
|description:|The metadata model for a printer extruder in print jobs.|
|estimated_material_volume|number<br><br>The amount in mm3 of filament remaining in the filament bay before the print started.|
|extruder_index*|number<br><br>The position of the extruder on the machine as list index. Numbered from left to right.|
|infill|PrintJobInfillMetadata{...}|
|initial_temperature|number<br><br>The temperature to which the nozzle needs to be heated for processing the material.|
|material|PrintJobMaterialMetadata{...}|
|nozzle_diameter|number($float)<br><br>The diameter of the nozzle for which the print was sliced.|
|original_material_volume|number<br><br>The original amount in mm3 of filament in the filament bay.|
|print_core_id|string<br><br>The type of print core inserted at this position, e.g. 'AA 0.4'.|
|temperature|number($float)<br><br>The current temperature of print core, degrees celsius|
|| }

PrintJobGeneratorMetadata{|   |   |
|---|---|
|description:|The metadata model for the generator of the print job.|
|build_date|string($date-time)<br><br>The date on which that application was built.|
|name|string<br><br>The name of the application used to generate the Gcode.|
|version|string<br><br>The version of the application used to generate the Gcode.|
|| }

PrintJobInfillMetadata{|   |   |
|---|---|
|description:|The metadata model for the infill of the print job.|
|density*|number<br><br>The density of the infill in percentage.|
|is_gradual*|boolean  <br>default: false<br><br>Whether the infill is gradual.|
|| }

PrintJobInstanceConfigurationChange{|   |   |
|---|---|
|description:|Model for the response to the configuration change response. This is used for the print job instance responses  <br>and adds extra fields that are not received from the printers.|
|index|number<br><br>The hotend slot or extruder index to change|
|is_overridable*|boolean<br><br>Whether the configuration change may be overridden, i.e. the print job may be started with the current configuration.|
|origin_id*|string<br><br>Original/current material guid or hotend id|
|origin_name|string<br><br>Original/current material name or hotend id|
|target_id*|string<br><br>Target material guid or hotend id|
|target_name|string<br><br>Target material name or hotend id|
|type_of_change|string<br><br>The type of configuration change.<br><br>Enum:  <br>Array [ 4 ]|
|| }

PrintJobInstancePrinterConfiguration{|   |   |
|---|---|
|description:|Contains the fields of the printer status that are part of the print job instance.|
|air_manager|ClusterPrinterAirManager{...}|
|generated_time|string($date-time)<br><br>The datetime when the object was generated on the server-side.|
|material_station|ClusterPrinterMaterialStation{...}|
|print_cores|[...]|
|| }

PrintJobInstanceReportResponse{|   |   |
|---|---|
|description:|Data returned in the Cloud print job endpoints, that represents a single instance of a print job.|
|assigned_to|string<br><br>The name of the printer this job is assigned to while being queued.|
|build_plate|ClusterPrinterBuildPlate{...}|
|cloud_job_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>Unique cloud ID of a print job if it originated in the cloud.It may be empty in case the user does not have access to the print job.|
|cluster_id*|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The unique cloud cluster ID of the printer this job is assigned to.|
|compatible_machine_families|[...]|
|configuration|[...]|
|configuration_changes_required|[...]|
|constraints|ClusterPrintJobConstraints{...}|
|created_at*|string($date-time)<br><br>The timestamp when the job was created in Cura Connect.|
|deleted_at|string($date-time)<br><br>The time when this print job was deleted.|
|force*|boolean<br><br>Allow this job to be printed despite of mismatching configurations.|
|hidden|boolean<br><br>When a print job is hidden it has been deleted from the cloud history and should not be returned by the API anymore.|
|impediments_to_printing|[...]|
|last_seen|number($float)<br><br>The number of seconds since this job was checked.|
|machine_variant*|string<br><br>The machine type that this job should be printed on.Coincides with the machine_type field of the printer object.<br><br>Enum:  <br>Array [ 10 ]|
|name*|string<br><br>The name of the print job. Usually the name of the .gcode file.|
|network_error_count|number<br><br>The number of errors encountered when requesting data for this print job.|
|owner|string<br><br>The name of the user who added the print job to Cura Connect.|
|owner_deleted|boolean<br><br>Set to true if the user who started the print job has been deleted.|
|owner_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The unique ID of the user who started the print job.|
|printed_on_uuid|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>UUID of the printer used to print this job.|
|printer_configuration|PrintJobInstancePrinterConfiguration{...}|
|printer_name|string<br><br>The human readable name of the printer this job is assigned to.|
|printer_uuid|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>UUID of the printer that the job is currently printing on or assigned to.|
|sent_from*|string<br><br>The type of client that sent the print job to the printer.<br><br>Enum:  <br>Array [ 4 ]|
|started*|boolean<br><br>Whether the job has started printing or not.|
|state*|string  <br>default: in_progress<br><br>The status of print jobs. Can be one of - in_progress, waiting, history.<br><br>Enum:  <br>Array [ 6 ]|
|status*|string<br><br>The status of the print job.<br><br>Enum:  <br>Array [ 28 ]|
|status_detail|string<br><br>Gives more detail about the status of the print job.<br><br>Enum:  <br>Array [ 9 ]|
|time_elapsed|number<br><br>The remaining printing time in seconds.|
|time_total*|number<br><br>The total printing time in seconds.|
|updated_at|string($date-time)<br><br>The timestamp when the job was last updated.|
|uuid*|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>UUID of this print job. Should be used for identification purposes.|
|| }

PrintJobInstanceResponse{|   |   |
|---|---|
|description:|Data returned in the Cloud print job endpoints, that represents a single instance of a print job.|
|assigned_to|string<br><br>The name of the printer this job is assigned to while being queued.|
|build_plate|ClusterPrinterBuildPlate{...}|
|cloud_job_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>Unique cloud ID of a print job if it originated in the cloud.It may be empty in case the user does not have access to the print job.|
|cluster_id*|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The unique cloud cluster ID of the printer this job is assigned to.|
|compatible_machine_families|[...]|
|configuration|[...]|
|configuration_changes_required|[...]|
|constraints|ClusterPrintJobConstraints{...}|
|created_at*|string($date-time)<br><br>The timestamp when the job was created in Cura Connect.|
|deleted_at|string($date-time)<br><br>The time when this print job was deleted.|
|force*|boolean<br><br>Allow this job to be printed despite of mismatching configurations.|
|impediments_to_printing|[...]|
|is_online*|boolean<br><br>Whether the cluster is currently connected to the cloud.|
|last_seen|number($float)<br><br>The number of seconds since this job was checked.|
|machine_variant*|string<br><br>The machine type that this job should be printed on.Coincides with the machine_type field of the printer object.<br><br>Enum:  <br>Array [ 10 ]|
|name*|string<br><br>The name of the print job. Usually the name of the .gcode file.|
|network_error_count|number<br><br>The number of errors encountered when requesting data for this print job.|
|note|string  <br>maxLength: 500<br><br>A note for the print job instance.|
|owner|string<br><br>The name of the user who added the print job to Cura Connect.|
|owner_deleted|boolean<br><br>Set to true if the user who started the print job has been deleted.|
|owner_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The unique ID of the user who started the print job.|
|preview_url|string  <br>pattern: /^[a-z]+:\/\/[^\s/$.?#].[^\s]*$/<br><br>The URL where to download a preview image from for this print job.|
|printed_on_uuid|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>UUID of the printer used to print this job.|
|printer_name|string<br><br>The human readable name of the printer this job is assigned to.|
|printer_uuid|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>UUID of the printer that the job is currently printing on or assigned to.|
|sent_from*|string<br><br>The type of client that sent the print job to the printer.<br><br>Enum:  <br>Array [ 4 ]|
|started*|boolean<br><br>Whether the job has started printing or not.|
|state*|string  <br>default: in_progress<br><br>The status of print jobs. Can be one of - in_progress, waiting, history.<br><br>Enum:  <br>Array [ 6 ]|
|status*|string<br><br>The status of the print job.<br><br>Enum:  <br>Array [ 28 ]|
|status_detail|string<br><br>Gives more detail about the status of the print job.<br><br>Enum:  <br>Array [ 9 ]|
|status_message|UserMessage{...}|
|time_elapsed|number<br><br>The remaining printing time in seconds.|
|time_remaining*|number<br><br>The amount of time seconds remaining for printing, in seconds. For waiting jobs, includes time before starting.|
|time_total*|number<br><br>The total printing time in seconds.|
|uuid*|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>UUID of this print job. Should be used for identification purposes.|
|| }

PrintJobInstanceUpdateRequest{|   |   |
|---|---|
|description:|Model for updating the note in a print job instance.|
|note|string  <br>maxLength: 500<br><br>A note for the print job instance.|
|| }

PrintJobMaterialMetadata{|   |   |
|---|---|
|description:|The metadata model for a material in print jobs.|
|brand|string<br><br>The brand of material in this print core, e.g. 'Ultimaker'.|
|color|string<br><br>The color of material in this print core, e.g. 'Blue'.|
|density|number($float)<br><br>The density of the material in g/cm3.|
|diameter|number($float)<br><br>The diameter of the material in mm3.|
|guid|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>The GUID of the material in this print core, e.g. '506c9f0d-e3aa-4bd4-b2d2-23e2425b1aa9'.|
|material|string<br><br>The type of material in this print core, e.g. 'PLA'.|
|weight|number($float)<br><br>The weight of the material in g.|
|| }

PrintJobMetadata{|   |   |
|---|---|
|description:|The metadata model for print jobs.|
|build_plate|PrintJobBuildPlateMetadata{...}|
|build_volume|PrintJobBuildVolumeMetadata{...}|
|extruders|[...]|
|flavor|string<br><br>The type of the g-code.<br><br>Enum:  <br>Array [ 3 ]|
|generator|PrintJobGeneratorMetadata{...}|
|header_version|string<br><br>The version of the g-code format.|
|machine_variant|string<br><br>The model of the printer for which the g-code was sliced.<br><br>Enum:  <br>Array [ 10 ]|
|print|PrintJobPrintMetadata{...}|
|| }

PrintJobPresetMetadata{|   |   |
|---|---|
|description:|Information about the Cura preset used when slicing the print job.|
|layer_height*|number($float)  <br>minimum: 0<br><br>Layer height from Cura slice parameters|
|quality|string<br><br>Cura quality value.|
|type|string<br><br>Cura intent value.|
|| }

PrintJobPrintMetadata{|   |   |
|---|---|
|description:|The metadata model for the build volume of the print job.|
|estimated_time|number<br><br>The estimated time in seconds the print takes.|
|groups|number<br><br>The number of object groups in the file. Only applies when 'one-at-a-time' feature is used in Cura.|
|has_adhesion|boolean<br><br>Whether the print job has adhesion.|
|has_support|boolean<br><br>Whether the print job has support.|
|max_size|PrintJobCoordinatesMetadata{...}|
|min_size|PrintJobCoordinatesMetadata{...}|
|preset|PrintJobPresetMetadata{...}|
|| }

PrintJobResponse{|   |   |
|---|---|
|description:|Model for the print job upload status served by the Cura Cloud API.|
|access_key|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>A key that allows anyone to retrieve the details of the print job for reprinting it later|
|attachments|[...]|
|content_type|string  <br>pattern: /^(application\|audio\|image\|message\|multipart\|text\|video\|x-token\|model)\/([^\s]+)$/<br><br>The content type of the print job.<br><br>Enum:  <br>Array [ 5 ]|
|download_url|string  <br>pattern: /^[a-z]+:\/\/[^\s/$.?#].[^\s]*$/<br><br>A URL to download the toolpath file from.|
|file_size|number  <br>maximum: 1073741824  <br>minimum: 0<br><br>The size of the uploaded print job.|
|generated_time|string($date-time)<br><br>The datetime when the object was generated on the server-side.|
|is_submitted|boolean<br><br>If set to True indicates that PrintJob was submitted|
|job_id*|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The secret unique ID, e.g. 'kBEeZWEifXbrXviO8mRYLx45P8k5lHVGs43XKvRniPg='.|
|job_name|string<br><br>The name of the print job.|
|library_project_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The ID of the Digital Library project.|
|metadata|PrintJobMetadata{...}|
|notes|string  <br>maxLength: 150<br><br>The notes left for a print file during submission.|
|parsing_status|string<br><br>A parsing status indicating if the backend has finished parsing the print job metadata.<br><br>Enum:  <br>Array [ 4 ]|
|preview_image_url|string  <br>pattern: /^[a-z]+:\/\/[^\s/$.?#].[^\s]*$/<br><br>A signed URL to the location of the print job preview image (only available for UFP files).|
|source_file_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The file ID of the source file that the print job is derived from.|
|status*|string<br><br>The status of the print job.<br><br>Enum:  <br>Array [ 6 ]|
|status_description|string<br><br>Contains more details about the status, e.g. the cause of failures.|
|submitter_name|string  <br>maxLength: 100  <br>minLength: 2  <br>pattern: /^[^_!¡÷?¿/\\+=@#$%ˆ&*(){}\|~<>;:[\]\n\t]{2,}$/  <br>x-pattern-error: NameInvalid<br><br>Name of the user who uploaded the print job via submission link|
|upload_url|string  <br>pattern: /^[a-z]+:\/\/[^\s/$.?#].[^\s]*$/<br><br>The one-time use URL where the toolpath must be uploaded to (only if status is uploading).|
|uploaded_at|string($date-time)<br><br>The time on which the print job was uploaded.|
|user_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The ID of the user that uploaded this print job.|
|username|string  <br>maxLength: 100  <br>minLength: 3  <br>pattern: /^[A-Za-z0-9]+(?:[ _.-][A-Za-z0-9]+)*$/  <br>x-pattern-error: usernameInvalid<br><br>The user's unique username.|
|| }

PrintRequestResponse{|   |   |
|---|---|
|description:|Model for the API response when sending a print job to a connected cluster.|
|generated_time|string($date-time)<br><br>The datetime when the object was generated on the server-side.|
|job_id*|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The secret unique ID, e.g. 'kBEeZWEifXbrXviO8mRYLx45P8k5lHVGs43XKvRniPg='.|
|job_instance_uuid*|string  <br>pattern: /^\{{0,1}[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}{0,1}$/<br><br>The job instance UUID, generated in the cloud and used in both the cloud and on the printer.|
|status*|string<br><br>The status of the print request.<br><br>Enum:  <br>Array [ 4 ]|
|| }

PrinterActionBodyRequest{|   |   |
|---|---|
|description:|Model holding the body arguments for a printer action.  <br>Goes together with PrinterActionPathRequest to determine the whole action sent to the API.|
|channel|string<br><br>Selected firmware update channel.<br><br>Enum:  <br>Array [ 3 ]|
|enabled|boolean<br><br>Set printer availability to be enabled or disabled|
|material_profile_id|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The unique ID of the requested material profile object.|
|name|string<br><br>New name for the printer for the 'rename' action.|
|pin_code|string  <br>pattern: /^[0-9A-Z]{6}$/<br><br>Pin code to lock the printer with.|
|schedule_update|boolean<br><br>True to schedule an update. False to cancel any scheduled update.|
|| }

PrinterMaintenanceCompletedLogEntriesResponse{|   |   |
|---|---|
|description:|The response model for the printer maintenance completed tasks.|
|completed_at*|string($date-time)<br><br>The timestamp that the task was completed.|
|task_codes|[...]|
|user_id*|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The ID of the user.|
|username*|string  <br>maxLength: 100  <br>minLength: 3  <br>pattern: /^[A-Za-z0-9]+(?:[ _.-][A-Za-z0-9]+)*$/  <br>x-pattern-error: usernameInvalid<br><br>The user's unique username.|
|| }

PrinterMaintenanceTaskRequest{|   |   |
|---|---|
|description:|A maintenance task that has been executed.|
|task_codes|[...]|
|| }

PrinterMaintenanceTaskResponse{|   |   |
|---|---|
|description:|A maintenance task must be done now or in the future.|
|due_date|string($date-time)<br><br>Predicted time when the task should be performed.|
|is_due*|boolean<br><br>True if the task is due now.|
|task_rule*|PrinterMaintenanceTaskRule{...}|
|| }

PrinterMaintenanceTaskRule{|   |   |
|---|---|
|description:|A rule which describes a reoccurring maintenance task.|
|code*|string<br><br>Task code identifying a type of task.<br><br>Enum:  <br>Array [ 43 ]|
|task_details|Union type not supported in OpenAPI v2. See x-oneOf property or use OpenAPI v3.{...}|
|| }

RegistrationResponse{|   |   |
|---|---|
|description:|Model for the registration confirmation response from the Cura Connect API to the API users.|
|cluster_id*|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The cluster unique ID as received from the confirm registration endpoint.|
|generated_time|string($date-time)<br><br>The datetime when the object was generated on the server-side.|
|host_name*|string  <br>maxLength: 64  <br>minLength: 3<br><br>The name of the printer as configured during the Wi-Fi setup. Used as identifier for end users.|
|| }

ResponseMeta{|   |   |
|---|---|
|description:|Model describing the 'meta' field on a JSONAPI response.|
|limit_reached|boolean<br><br>A boolean indicating whether the maximum number of results has been reached. Please upgrade your subscription to see all the data.|
|page|PaginationMetadata{...}|
|| }

TimeBasedDetail{|   |   |
|---|---|
|description:|Details for a clock time based reoccurring maintenance task.|
|interval*|number  <br>minimum: 0<br><br>Describes the time in seconds between recommended execution this task.|
|| }

UserMessage{|   |   |
|---|---|
|description:|Model for messages sent by a user.|
|body|string  <br>maxLength: 1000<br><br>The body of the message.|
|generated_time|string($date-time)<br><br>The datetime when the object was generated on the server-side.|
|user_id*|string  <br>maxLength: 44  <br>minLength: 44  <br>pattern: /^[A-Za-z0-9-_]*={0,3}$/<br><br>The ID of the user that created this message.|
|username|string  <br>maxLength: 100  <br>minLength: 3  <br>pattern: /^[A-Za-z0-9]+(?:[ _.-][A-Za-z0-9]+)*$/  <br>x-pattern-error: usernameInvalid<br><br>The username of the user that created this message. If user name is null, the user was deleted.|
|| }

WebcamSnapshotStatus{|   |   |
|---|---|
|description:|Action response contains the URL of the webcam snapshot.|
|image_url*|string  <br>pattern: /^[a-z]+:\/\/[^\s/$.?#].[^\s]*$/<br><br>URL of the image. Only valid if 'status' is SUCCESS|
|| }