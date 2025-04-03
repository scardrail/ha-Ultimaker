REST API for the Ultimaker 3D printer.

Authentication: Any PUT/POST/DELETE api requires authentication before it can be used. Authentication is done with http digest (RFC 2617) without fallback to basic authentication.

To get a valid username/password combination, the following process can/should be followed.

1) POST /auth/request with 'application' and 'user' as parameters. The application name and user name will be shown to the user on the printer. The reply body will contain a json reply with an 'id' and 'key' part.

2) Repeatedly GET /auth/check/ until it reports 'authorized' or 'unauthorized'. This will be reported back once the end user selects if the application is allowed to use the API.

3) [optional] test the authentication, the earlier given 'id' is the username, the 'key' is the password. Use digest authentication on GET /auth/verify to test this.

Authentication : Request and check authorization keysShow/HideList OperationsExpand Operations
post /auth/request
Implementation Notes
Request authentication from the printer. This generates new id/key combination that has to be used as username/password in the digest authentication on certain APIs.

Response Class (Status 200)
Register as a new application that wants access to the API.

ModelExample Value
{
  "id": "string",
  "key": "string"
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
application	
(required)
Name of the application that wants access. Displayed to the user.

formData	string
user	
(required)
Name of the user who wants access. Displayed to the user when confirming access.

formData	string
host_name	
Optionally the hostname of the service that is authenticating can be provided for future use.

formData	string
exclusion_key	
Optionally This key can make sure only one authorisation will exist on the remote printer with this same key, This allows a new user to de-authenticate the old one preventing multiple printer controlling applications to use the printer at the same time. Naturally multiple authorisations can exist if this is omitted

formData	string
get /auth/check/{id}
Implementation Notes
Check if the given ID is authorized for printer access. Will return 'authorized' when the end user has selected that this application is allowed to use the printer. Will return 'unauthorized' when the user has selected that the application is not allowed to access the printer. Will return 'unknown' when the end user has not selected any option yet.

Response Class (Status 200)
result of the authorization check.

ModelExample Value
{
  "message": "authorized"
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
id	
(required)
id returned from the /auth/request call

path	string
get /auth/verify
Implementation Notes
This API call always does authentication checking for digest authentication. Invalid digest id/key combinations will generate a 401 result.

Response Class (Status 200)
Verify check successful, digest authentication is valid.

ModelExample Value
{
  "message": "ok"
}


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
401	
Not authorized. Check or request your id/key combination, and/or http digest implementation.

Materials : All materials known by the printerShow/HideList OperationsExpand Operations
get /materials
Response Class (Status 200)
All known material XML files, one string for each material.

ModelExample Value
[
  "string"
]


Response Content Type 
application/json
post /materials
Parameters
Parameter	Value	Description	Parameter Type	Data Type
file	Aucun fichier choisi	
Material file (.xml)

formData	file
filename	
(required)
Name of the file

formData	string
signature_file	Aucun fichier choisi
Signature file (.sig)

formData	file
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Material profile added.

delete /materials/{material_guid}
Parameters
Parameter	Value	Description	Parameter Type	Data Type
material_guid	
(required)
GUID of material to delete

path	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Material deleted

get /materials/{material_guid}
Response Class (Status 200)
string


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
material_guid	
(required)
GUID of material to fetch

path	string
put /materials/{material_guid}
Parameters
Parameter	Value	Description	Parameter Type	Data Type
material_guid	
(required)
GUID of material to update

path	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Material updated

Printer : Printer stateShow/HideList OperationsExpand Operations
get /printer
Implementation Notes
Returns printer object

Response Class (Status 200)
Printer object

ModelExample Value
{
  "heads": [
    {
      "position": {
        "x": 0,
        "y": 0,
        "z": 0
      },
      "max_speed": {
        "x": 0,
        "y": 0,
        "z": 0
      },
      "acceleration": 0,
      "jerk": {
        "x": 0,
        "y": 0,
        "z": 0
      },
      "extruders": [
        {
          "hotend": {
            "id": "string",
            "serial": "string",
            "temperature": {
              "target": 0,
              "current": 0
            },
            "offset": {
              "x": 0,
              "y": 0,
              "z": 0,
              "state": "valid"
            },
            "statistics": {
              "last_material_guid": "string",
              "material_extruded": 0,
              "max_temperature_exposed": 0,
              "time_spent_hot": 0
            }
          },
          "feeder": {
            "position": 0,
            "max_speed": 0,
            "jerk": 0,
            "acceleration": 0
          },
          "active_material": {
            "length_remaining": 0,
            "GUID": "string"
          }
        }
      ],
      "fan": 0
    }
  ],
  "camera": {
    "feed": "string"
  },
  "bed": {
    "type": "string",
    "temperature": {
      "target": 0,
      "current": 0
    },
    "pre_heat": {
      "temperature": 0,
      "timeout": 0
    }
  },
  "network": {
    "wifi": {
      "connected": true,
      "enabled": true,
      "mode": "AUTO",
      "ssid": "string"
    },
    "wifi_networks": [
      {
        "ssid": "string",
        "security_required": true,
        "strength": 0
      }
    ],
    "ethernet": {
      "connected": true,
      "enabled": true
    }
  },
  "led": {
    "hue": 0,
    "saturation": 0,
    "brightness": 0
  },
  "status": "booting",
  "airmanager": {
    "firmware_version": "string",
    "filter_age": 0,
    "filter_max_age": 0,
    "filter_status": "unknown",
    "status": "error",
    "fan_speed": 0
  }
}


Response Content Type 
application/json
get /printer/diagnostics/cap_sensor_noise
Implementation Notes
Calculates noise variances on the cap sensor by measuring the sensor data and calculating the noise

Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
A list of dictionaries containing the min, max, avg and stddev^2 values

400	
When a timeout occurs (taking too long to get the data) or when the printer is already busy

get /printer/diagnostics/temperature_flow/{sample_count}
Implementation Notes
Gets historical temperature & flow data

Parameters
Parameter	Value	Description	Parameter Type	Data Type
sample_count	
(required)
The number of samples to get

path	integer
csv	
If not zero, return the results as comma separated values instead of a normal json response.

query	integer
max_timestamp	
If specified, an older data set can be retrieved by specifying the oldest timestamp of any previously returned data

query	double
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
A 2 dimensional array of sample data. First row of the array contains names of each column. All the other rows contain the actual sample data.

get /printer/diagnostics/probing_report
Response Class (Status 200)
file


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
When no probing report is found.

get /printer/status
Implementation Notes
Get the status of the printer

Response Class (Status 200)
Global status of the printer, most interesting ones are 'idle' which means the printer can accept a print job. And 'printing' which means the printer is actively working on a print job.

ModelExample Value
"booting"


Response Content Type 
application/json
get /printer/led
Implementation Notes
Returns the hue, saturation, and value (HSV) of the case lighting

Response Class (Status 200)
HSV the case lighting

ModelExample Value
{
  "hue": 0,
  "saturation": 0,
  "brightness": 0
}


Response Content Type 
application/json
put /printer/led
Implementation Notes
Sets the hue, saturation, and value (HSV) of the case lighting

Parameters
Parameter	Value	Description	Parameter Type	Data Type
color	
(required)

Parameter content type: 
application/json
Target HSV of case lighting

body	
ModelExample Value
{
  "hue": 0,
  "saturation": 0,
  "brightness": 0
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
lighting set

get /printer/led/hue
Implementation Notes
Returns the hue of the case lighting

Response Class (Status 200)
Current hue of the case lighting

ModelExample Value
0


Response Content Type 
application/json
put /printer/led/hue
Parameters
Parameter	Value	Description	Parameter Type	Data Type
hue	
(required)

Parameter content type: 
application/json
Target hue of case lighting

body	led_hue {
number
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
lighting set

get /printer/led/saturation
Implementation Notes
Returns the saturation of the case lighting

Response Class (Status 200)
Current saturation of the case lighting

ModelExample Value
0


Response Content Type 
application/json
put /printer/led/saturation
Parameters
Parameter	Value	Description	Parameter Type	Data Type
saturation	
(required)

Parameter content type: 
application/json
Target saturation of case lighting

body	led_saturation {
number
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
lighting set

get /printer/led/brightness
Implementation Notes
Returns the brightness of the case lighting

Response Class (Status 200)
Current brightness of the case lighting

ModelExample Value
0


Response Content Type 
application/json
put /printer/led/brightness
Parameters
Parameter	Value	Description	Parameter Type	Data Type
value	
(required)

Parameter content type: 
application/json
Target brightness of case lighting

body	led_brightness {
number
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
lighting set

post /printer/led/blink
Parameters
Parameter	Value	Description	Parameter Type	Data Type
blink	

Parameter content type: 
application/json
body	
ModelExample Value
{
  "frequency": 0,
  "count": 0
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
blink set

400	
This is returned when frequency <= 0 or count <= 0 with a message

get /printer/heads
Implementation Notes
Returns all heads of the printer

Response Class (Status 200)
ModelExample Value
[
  {
    "position": {
      "x": 0,
      "y": 0,
      "z": 0
    },
    "max_speed": {
      "x": 0,
      "y": 0,
      "z": 0
    },
    "acceleration": 0,
    "jerk": {
      "x": 0,
      "y": 0,
      "z": 0
    },
    "extruders": [
      {
        "hotend": {
          "id": "string",
          "serial": "string",
          "temperature": {
            "target": 0,
            "current": 0
          },
          "offset": {
            "x": 0,
            "y": 0,
            "z": 0,
            "state": "valid"
          },
          "statistics": {
            "last_material_guid": "string",
            "material_extruded": 0,
            "max_temperature_exposed": 0,
            "time_spent_hot": 0
          }
        },
        "feeder": {
          "position": 0,
          "max_speed": 0,
          "jerk": 0,
          "acceleration": 0
        },
        "active_material": {
          "length_remaining": 0,
          "GUID": "string"
        }
      }
    ],
    "fan": 0
  }
]


Response Content Type 
application/json
get /printer/heads/{head_id}
Implementation Notes
Returns head by ID

Response Class (Status 200)
ModelExample Value
{
  "position": {
    "x": 0,
    "y": 0,
    "z": 0
  },
  "max_speed": {
    "x": 0,
    "y": 0,
    "z": 0
  },
  "acceleration": 0,
  "jerk": {
    "x": 0,
    "y": 0,
    "z": 0
  },
  "extruders": [
    {
      "hotend": {
        "id": "string",
        "serial": "string",
        "temperature": {
          "target": 0,
          "current": 0
        },
        "offset": {
          "x": 0,
          "y": 0,
          "z": 0,
          "state": "valid"
        },
        "statistics": {
          "last_material_guid": "string",
          "material_extruded": 0,
          "max_temperature_exposed": 0,
          "time_spent_hot": 0
        }
      },
      "feeder": {
        "position": 0,
        "max_speed": 0,
        "jerk": 0,
        "acceleration": 0
      },
      "active_material": {
        "length_remaining": 0,
        "GUID": "string"
      }
    }
  ],
  "fan": 0
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head to fetch

path	long
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
Head was not found. Note that this means that all deeper (eg: getting position, extruders, etc.) calls will also return a 404

get /printer/heads/{head_id}/position
Implementation Notes
Returns position of head by ID

Response Class (Status 200)
ModelExample Value
{
  "x": 0,
  "y": 0,
  "z": 0
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head of which to get position. Note that this position also has a Z component. This api assumes that the head is the only part that moves.

path	long
post /printer/heads/{head_id}/position
Implementation Notes
A POST to the position is used to specific actions for the position.

Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the hotend is fetched

path	long
action	
(required)

Parameter content type: 
application/json
Which action to do on the position. Currently a single action is supported 'home', which sends the head to the endstop positions and resets the origin of the position so 0,0,0 is the front left corner on the print bed.

body	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
Position set

put /printer/heads/{head_id}/position
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the position is changed

path	long
position	
(required)

Parameter content type: 
application/json
Target position

body	
ModelExample Value
{
  "x": 0,
  "y": 0,
  "z": 0,
  "speed": 150
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Position set

get /printer/heads/{head_id}/max_speed
Implementation Notes
Returns max speed of head by ID

Response Class (Status 200)
ModelExample Value
{
  "x": 0,
  "y": 0,
  "z": 0
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head of which to get the max speed of. Note that this speed also has a Z component. This api assumes that the head is the only part that moves.

path	long
put /printer/heads/{head_id}/max_speed
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
path	long
speed	
(required)

Parameter content type: 
application/json
Target maximum speed for each axis.

body	
ModelExample Value
{
  "x": 0,
  "y": 0,
  "z": 0
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Max speed set

get /printer/heads/{head_id}/acceleration
Implementation Notes
Returns the default acceleration of head by ID.

Response Class (Status 200)
number


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head of which to get the default acceleration of. Note that this speed also has a Z component. This API assumes that the head is the only part that moves.

path	long
put /printer/heads/{head_id}/acceleration
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
path	long
acceleration	
(required)

Parameter content type: 
application/json
Target default acceleration.

body	double
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
acceleration speed set

get /printer/heads/{head_id}/jerk
Implementation Notes
Returns jerk of head by ID

Response Class (Status 200)
ModelExample Value
{
  "x": 0,
  "y": 0,
  "z": 0
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head of which to get the jerk of. Note that this speed also has a Z component. This API assumes that the head is the only part that moves.

path	long
put /printer/heads/{head_id}/jerk
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
path	long
jerk	
(required)

Parameter content type: 
application/json
Target jerk

body	
ModelExample Value
{
  "x": 0,
  "y": 0,
  "z": 0
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Jerk set

get /printer/bed
Implementation Notes
Returns bed object

Response Class (Status 200)
bed object

ModelExample Value
{
  "type": "string",
  "temperature": {
    "target": 0,
    "current": 0
  },
  "pre_heat": {
    "temperature": 0,
    "timeout": 0
  }
}


Response Content Type 
application/json
get /printer/bed/temperature
Implementation Notes
Returns temperature of bed

Response Class (Status 200)
Temperature of the bed

ModelExample Value
{
  "target": 0,
  "current": 0
}


Response Content Type 
application/json
put /printer/bed/temperature
Parameters
Parameter	Value	Description	Parameter Type	Data Type
temperature	
(required)
Target temperature of bed

formData	double
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Temperature set

get /printer/bed/pre_heat
Implementation Notes
Returns status of pre-heating the heated bed.

Response Class (Status 200)
Status of pre-heating the heated bed.

ModelExample Value
{
  "active": true,
  "remaining": 0
}


Response Content Type 
application/json
put /printer/bed/pre_heat
Parameters
Parameter	Value	Description	Parameter Type	Data Type
temperature	
(required)

Parameter content type: 
application/json
body	
ModelExample Value
{
  "temperature": 0,
  "timeout": 0
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Preheating Temperature set

400	
Bad request (invalid parameters)

get /printer/bed/type
Implementation Notes
Returns the type of the bed.

Response Class (Status 200)
string


Response Content Type 
application/json
get /printer/heads/{head_id}/extruders
Implementation Notes
Returns all extruders of a head

Response Class (Status 200)
ModelExample Value
[
  {
    "hotend": {
      "id": "string",
      "serial": "string",
      "temperature": {
        "target": 0,
        "current": 0
      },
      "offset": {
        "x": 0,
        "y": 0,
        "z": 0,
        "state": "valid"
      },
      "statistics": {
        "last_material_guid": "string",
        "material_extruded": 0,
        "max_temperature_exposed": 0,
        "time_spent_hot": 0
      }
    },
    "feeder": {
      "position": 0,
      "max_speed": 0,
      "jerk": 0,
      "acceleration": 0
    },
    "active_material": {
      "length_remaining": 0,
      "GUID": "string"
    }
  }
]


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the extruders are fetched

path	long
get /printer/heads/{head_id}/extruders/{extruder_id}
Implementation Notes
Returns extruder by ID

Response Class (Status 200)
ModelExample Value
{
  "hotend": {
    "id": "string",
    "serial": "string",
    "temperature": {
      "target": 0,
      "current": 0
    },
    "offset": {
      "x": 0,
      "y": 0,
      "z": 0,
      "state": "valid"
    },
    "statistics": {
      "last_material_guid": "string",
      "material_extruded": 0,
      "max_temperature_exposed": 0,
      "time_spent_hot": 0
    }
  },
  "feeder": {
    "position": 0,
    "max_speed": 0,
    "jerk": 0,
    "acceleration": 0
  },
  "active_material": {
    "length_remaining": 0,
    "GUID": "string"
  }
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the extruder is fetched

path	long
extruder_id	
(required)
ID of extruder to fetch.

path	long
get /printer/heads/{head_id}/extruders/{extruder_id}/hotend/offset
Implementation Notes
Returns offset of hotend with respect to head

Response Class (Status 200)
ModelExample Value
{
  "x": 0,
  "y": 0,
  "z": 0,
  "state": "valid"
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the extruder is fetched

path	long
extruder_id	
(required)
ID of extruder to fetch

path	long
get /printer/heads/{head_id}/extruders/{extruder_id}/feeder
Implementation Notes
Returns feeder of selected extruder

Response Class (Status 200)
ModelExample Value
{
  "position": 0,
  "max_speed": 0,
  "jerk": 0,
  "acceleration": 0
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the extruder is fetched

path	long
extruder_id	
(required)
ID of extruder from which the feeder is fetched

path	long
get /printer/heads/{head_id}/extruders/{extruder_id}/feeder/jerk
Implementation Notes
Returns jerk of feeder

Response Class (Status 200)
number


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the extruder is fetched

path	long
extruder_id	
(required)
ID of extruder from which the feeder is fetched

path	long
put /printer/heads/{head_id}/extruders/{extruder_id}/feeder/jerk
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the extruder is fetched

path	long
extruder_id	
(required)
ID of extruder from which the feeder is fetched

path	long
jerk	
(required)

Parameter content type: 
application/json
Target jerk

body	double
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Jerk set

get /printer/heads/{head_id}/extruders/{extruder_id}/feeder/max_speed
Implementation Notes
Returns max_speed of feeder.

Response Class (Status 200)
number


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the extruder is fetched

path	long
extruder_id	
(required)
ID of extruder from which the feeder is fetched

path	long
put /printer/heads/{head_id}/extruders/{extruder_id}/feeder/max_speed
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the extruder is fetched

path	long
extruder_id	
(required)
ID of extruder from which the feeder is fetched

path	long
max_speed	
(required)

Parameter content type: 
application/json
Target max speed

body	double
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Max speed set

get /printer/heads/{head_id}/extruders/{extruder_id}/feeder/acceleration
Implementation Notes
Returns acceleration of feeder.

Response Class (Status 200)
number


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the extruder is fetched

path	long
extruder_id	
(required)
ID of extruder from which the feeder is fetched

path	long
put /printer/heads/{head_id}/extruders/{extruder_id}/feeder/acceleration
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the extruder is fetched

path	long
extruder_id	
(required)
ID of extruder from which the feeder is fetched

path	long
acceleration	
(required)

Parameter content type: 
application/json
Target acceleration speed

body	double
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Acceleration set

get /printer/heads/{head_id}/extruders/{extruder_id}/active_material
Implementation Notes
Get the active material of the extruder

Response Class (Status 200)
ModelExample Value
{
  "length_remaining": 0,
  "GUID": "string"
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the extruder is fetched

path	long
extruder_id	
(required)
ID of extruder

path	long
get /printer/heads/{head_id}/extruders/{extruder_id}/active_material/length_remaining
Implementation Notes
length of material remaining on spool in mm. Or -1 if no value is known.

Response Class (Status 200)
number


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the hotend is fetched

path	long
extruder_id	
(required)
ID of extruder from which the hotend is fetched

path	long
get /printer/heads/{head_id}/extruders/{extruder_id}/hotend
Implementation Notes
Returns hotend of extruder

Response Class (Status 200)
ModelExample Value
{
  "id": "string",
  "serial": "string",
  "temperature": {
    "target": 0,
    "current": 0
  },
  "offset": {
    "x": 0,
    "y": 0,
    "z": 0,
    "state": "valid"
  },
  "statistics": {
    "last_material_guid": "string",
    "material_extruded": 0,
    "max_temperature_exposed": 0,
    "time_spent_hot": 0
  }
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the hotend is fetched

path	long
extruder_id	
(required)
ID of extruder from which the hotend is fetched

path	long
get /printer/heads/{head_id}/extruders/{extruder_id}/hotend/temperature
Implementation Notes
Returns temperature of extruder

Response Class (Status 200)
Temperature of the hotend

ModelExample Value
{
  "target": 0,
  "current": 0
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the hotend is fetched

path	long
extruder_id	
(required)
ID of extruder from which the hotend is fetched

path	long
put /printer/heads/{head_id}/extruders/{extruder_id}/hotend/temperature
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the hotend is fetched

path	long
extruder_id	
(required)
ID of extruder from which the hotend is fetched

path	long
temperature	
(required)
Target temperature of nozzle

formData	double
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Temperature set

get /printer/heads/{head_id}/extruders/{extruder_id}/active_material/guid
Implementation Notes
Returns the GUID of the active material

Response Class (Status 200)
string


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the hotend is fetched

path	long
extruder_id	
(required)
ID of extruder from which the hotend is fetched

path	long
get /printer/heads/{head_id}/extruders/{extruder_id}/active_material/GUID
Warning: Deprecated
Implementation Notes
Returns the GUID of the active material

Response Class (Status 200)
string


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
head_id	
(required)
ID of head from which the hotend is fetched

path	long
extruder_id	
(required)
ID of extruder from which the hotend is fetched

path	long
post /printer/validate_header
Response Class (Status 200)
All header validation mishaps

ModelExample Value
[
  {
    "fault_code": "HEADER_NOT_PRESENT",
    "fault_level": "WARNING",
    "message": "string",
    "data": "string"
  }
]


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
file	Aucun fichier choisi	
File that needs to be printed (.gcode, .gcode.gz)

formData	file
Response Messages
HTTP Status Code	Reason	Response Model	Headers
400	
No validation checked because file is missing.

Network : Network stateShow/HideList OperationsExpand Operations
get /printer/network
Implementation Notes
Returns network state

Response Class (Status 200)
Network object

ModelExample Value
{
  "wifi": {
    "connected": true,
    "enabled": true,
    "mode": "AUTO",
    "ssid": "string"
  },
  "wifi_networks": [
    {
      "ssid": "string",
      "security_required": true,
      "strength": 0
    }
  ],
  "ethernet": {
    "connected": true,
    "enabled": true
  }
}


Response Content Type 
application/json
get /printer/network/wifi_networks
Implementation Notes
Returns a list of available wifi networks

Response Class (Status 200)
List of network ssid'

ModelExample Value
[
  {
    "ssid": "string",
    "security_required": true,
    "strength": 0
  }
]


Response Content Type 
application/json
delete /printer/network/wifi_networks/{ssid}
Implementation Notes
Forget a wifi network

Parameters
Parameter	Value	Description	Parameter Type	Data Type
ssid	
(required)
ssid of the network to forget.

path	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204		
put /printer/network/wifi_networks/{ssid}
Implementation Notes
Connect to a wifi network

Parameters
Parameter	Value	Description	Parameter Type	Data Type
ssid	
(required)
ssid of the network to connect with.

path	string
passphrase	
(required)
Passphrase of network to connect with

formData	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204		
PrintJob : Currently running printShow/HideList OperationsExpand Operations
get /print_job
Response Class (Status 200)
Print job object

ModelExample Value
{
  "time_elapsed": 0,
  "time_total": 0,
  "datetime_started": "2025-04-03T08:32:50.691Z",
  "datetime_finished": "2025-04-03T08:32:50.691Z",
  "datetime_cleaned": "2025-04-03T08:32:50.691Z",
  "source": "string",
  "source_user": "string",
  "source_application": "string",
  "name": "string",
  "uuid": "string",
  "reprint_original_uuid": "string",
  "progress": 0,
  "state": "none",
  "result": "Failed"
}


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

post /print_job
Response Class (Status 201)
Print job accepted

ModelExample Value
{
  "message": "string",
  "uuid": "string"
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
jobname	
(required)
Name of the print job.

formData	string
file	Aucun fichier choisi	
File that needs to be printed (.gcode, .gcode.gz, .ufp)

formData	file
owner	
The name of the owner of the print.

formData	string
created_at	
The moment of creation of the printjob.

formData	date-time
get /print_job/name
Implementation Notes
Name of print job

Response Class (Status 200)
string


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/datetime_started
Implementation Notes
The moment the current print job was started

Response Class (Status 200)
date-time


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/datetime_finished
Implementation Notes
The moment the last print job finished.

Response Class (Status 200)
date-time


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/datetime_cleaned
Implementation Notes
The moment the last print job was cleaned from the build plate

Response Class (Status 200)
date-time


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/source
Implementation Notes
From what source was the print job started. USB means it's started manually from the USB drive. WEB_API means it's being received by the WEB API. CALIBRATION_MENU means it's printing the XY offset print

Response Class (Status 200)
string


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/source_user
Implementation Notes
If the origin equals to WEB_API, then this will return the user who initiated the job

Response Class (Status 200)
string


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/source_application
Implementation Notes
If the origin equals to WEB_API, then this will return the application that sent the job

Response Class (Status 200)
string


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/uuid
Response Class (Status 200)
Unique identifier of this print job. In a UUID4 format.

ModelExample Value
"string"


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/reprint_original_uuid
Response Class (Status 200)
Unique identifier of this print job. In a UUID4 format.

ModelExample Value
"string"


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/time_elapsed
Implementation Notes
Get the time elapsed (in seconds) since starting this print, including pauses etc.

Response Class (Status 200)
integer


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/time_total
Implementation Notes
Get the (estimated) total time in seconds for this print, excluding pauses etc.

Response Class (Status 200)
integer


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/progress
Implementation Notes
Get the (estimated) progress for the current print job, a value between 0 and 1

Response Class (Status 200)
number


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/gcode
Response Class (Status 200)
file


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running or no gcode found

get /print_job/container
Response Class (Status 200)
file


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running or no file found

get /print_job/pause_source
Implementation Notes
If the printer is paused this exposes what initiated the pause

Response Class (Status 200)
string


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

get /print_job/state
Implementation Notes
Get the print job state

Response Class (Status 200)
string


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

put /print_job/state
Parameters
Parameter	Value	Description	Parameter Type	Data Type
target	
(required)

Parameter content type: 
application/json
"print", "pause" or "abort". Change the current state of the print. Note that only changes to abort / pause are always allowed and changing to print only when state is paused.

body	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
State changed

get /print_job/result
Implementation Notes
The result of the current print job

Response Class (Status 200)
The result of a print job

ModelExample Value
"Failed"


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
No printer job running

System : Device informationShow/HideList OperationsExpand Operations
get /system
Implementation Notes
Get the entire system object

Response Class (Status 200)
ModelExample Value
{
  "name": "string",
  "platform": "string",
  "hostname": "string",
  "firmware": "string",
  "country": "string",
  "language": "string",
  "uptime": 0,
  "time": {
    "utc": 0
  },
  "type": "string",
  "variant": "string",
  "memory": {
    "total": 0,
    "used": 0
  },
  "hardware": {
    "typeid": 0,
    "revision": 0
  },
  "log": "string",
  "guid": "string"
}


Response Content Type 
application/json
get /system/platform
Implementation Notes
A string identifying the underlying platform in human readable form.

Response Class (Status 200)
string


Response Content Type 
application/json
get /system/hostname
Implementation Notes
The hostname of this machine

Response Class (Status 200)
string


Response Content Type 
application/json
get /system/firmware
Implementation Notes
The version of the firmware currently running

Response Class (Status 200)
string


Response Content Type 
application/json
put /system/firmware
Implementation Notes
Trigger a firmware update. Printer will try to fetch & install the latest version.

Parameters
Parameter	Value	Description	Parameter Type	Data Type
update_type	

Parameter content type: 
application/json
Type of the firmware update to do. Can be 'latest' or 'stable'

body	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
Update started

get /system/firmware/status
Implementation Notes
Get the status of the firmware update

Response Class (Status 200)
string


Response Content Type 
application/json
get /system/firmware/stable
Implementation Notes
Get the version available for updating in the 'stable' release path, if you are subscibed to this channel

Response Class (Status 200)
string


Response Content Type 
application/json
get /system/firmware/latest
Implementation Notes
Get the version available for updating in the 'latest' release path, if you are subscibed to this channel

Response Class (Status 200)
string


Response Content Type 
application/json
get /system/memory
Implementation Notes
The current memory usage

Response Class (Status 200)
Memory usage

ModelExample Value
{
  "total": 0,
  "used": 0
}


Response Content Type 
application/json
get /system/time
Implementation Notes
The current UTC time

Response Class (Status 200)
Time

ModelExample Value
{
  "utc": 0
}


Response Content Type 
application/json
get /system/log
Implementation Notes
Get the logs of the system

Response Class (Status 200)
Log data

ModelExample Value
[
  "string"
]


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
boot	
Allow a boot parameter to get logs from previous boot sessions, default is 0 which is the current boot. -1 is the previous boot.

query	double
lines	
Allow a lines parameter to specify the number of lines to get from the log. Defaults to 50

query	double
get /system/name
Implementation Notes
Get the name of the system

Response Class (Status 200)
string


Response Content Type 
application/json
put /system/name
Parameters
Parameter	Value	Description	Parameter Type	Data Type
name	
(required)

Parameter content type: 
application/json
Target name of machine

body	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Name set

400	
Name is not set, because an invalid name is specified

get /system/country
Implementation Notes
Get the country of the system

Response Class (Status 200)
string


Response Content Type 
application/json
put /system/country
Parameters
Parameter	Value	Description	Parameter Type	Data Type
country	
(required)

Parameter content type: 
application/json
Target country of system

body	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
204	
Country set

get /system/is_country_locked
Implementation Notes
Is the country locked for this system?

Response Class (Status 200)
boolean


Response Content Type 
application/json
get /system/language
Implementation Notes
Get the language of the system

Response Class (Status 200)
string


Response Content Type 
application/json
get /system/uptime
Implementation Notes
Get the uptime of the system in seconds

Response Class (Status 200)
integer


Response Content Type 
application/json
get /system/type
Implementation Notes
Get the type of machine that we are talking with. Always returns "3D printer"

Response Class (Status 200)
string


Response Content Type 
application/json
get /system/variant
Implementation Notes
Gets the machines variant. Currently this can return "Ultimaker 3", "Ultimaker 3 extended" or "Ultimaker S5".

Response Class (Status 200)
string


Response Content Type 
application/json
get /system/hardware
Implementation Notes
Gets the hardware number and revision identifiers

Response Class (Status 200)
Machine hardware type and revision ID

ModelExample Value
{
  "typeid": 0,
  "revision": 0
}


Response Content Type 
application/json
get /system/hardware/typeid
Implementation Notes
Gets the machine type as number identifier. This identifier IDs a specific form of hardware

Response Class (Status 200)
integer


Response Content Type 
application/json
get /system/hardware/revision
Implementation Notes
The same machine could have different hardware revisions. When hardware is updated and software needs to know that hardware has changed, this revision number is changed. Currently only revision 0 is known.

Response Class (Status 200)
integer


Response Content Type 
application/json
get /system/guid
Implementation Notes
Every machine has a unique identifier stored inside the board. This allows for unique identification of this machine. This identifier is a UUID4.

Response Class (Status 200)
string


Response Content Type 
application/json
put /system/display_message
Implementation Notes
Enable external services to display a message screen on the printer.

Parameters
Parameter	Value	Description	Parameter Type	Data Type
message_data	
(required)

Parameter content type: 
application/json
Data to display on the screen of the printer.

body	
ModelExample Value
{
  "message": "string",
  "button_caption": "string"
}
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
Message is being displayed on the printer.

400	
No message specified.

405	
Message cannot be displayed because the printer is busy.

History : History of this printerShow/HideList OperationsExpand Operations
get /history/print_jobs
Response Class (Status 200)
All past PrintJobs on this printer

ModelExample Value
[
  {
    "created_at": "2025-04-03T08:32:50.764Z",
    "extruders_used": {},
    "generator_version": "string",
    "has_ppr": true,
    "interrupted_step": "string",
    "material_0_amount": 0,
    "material_1_amount": 0,
    "material_0_guid": "string",
    "material_1_guid": "string",
    "owner": "string",
    "printcore_0_name": "string",
    "printcore_1_name": "string",
    "slice_uuid": "string",
    "time_elapsed": 0,
    "time_estimated": 0,
    "time_total": 0,
    "datetime_started": "2025-04-03T08:32:50.764Z",
    "datetime_finished": "2025-04-03T08:32:50.764Z",
    "datetime_cleaned": "2025-04-03T08:32:50.764Z",
    "result": "Finished",
    "source": "string",
    "reprint_original_uuid": "string",
    "name": "string",
    "uuid": "string"
  }
]


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
offset	
Allow an offset parameter to specify the start in the history to get jobs from. Defaults to 0

query	double
count	
Allow a count parameter to specify the number of jobs to get from the log. Defaults to 50

query	double
get /history/print_jobs/{uuid}
Response Class (Status 200)
PrintJob with the given UUID

ModelExample Value
{
  "created_at": "2025-04-03T08:32:50.773Z",
  "extruders_used": {},
  "generator_version": "string",
  "has_ppr": true,
  "interrupted_step": "string",
  "material_0_amount": 0,
  "material_1_amount": 0,
  "material_0_guid": "string",
  "material_1_guid": "string",
  "owner": "string",
  "printcore_0_name": "string",
  "printcore_1_name": "string",
  "slice_uuid": "string",
  "time_elapsed": 0,
  "time_estimated": 0,
  "time_total": 0,
  "datetime_started": "2025-04-03T08:32:50.773Z",
  "datetime_finished": "2025-04-03T08:32:50.773Z",
  "datetime_cleaned": "2025-04-03T08:32:50.773Z",
  "result": "Finished",
  "source": "string",
  "reprint_original_uuid": "string",
  "name": "string",
  "uuid": "string"
}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
uuid	
(required)
UUID of the job to get

path	string
get /history/events
Response Class (Status 200)
All events that happened on this printer

ModelExample Value
[
  {
    "time": "2025-04-03T08:32:50.777Z",
    "type_id": 0,
    "message": "string",
    "parameters": [
      "string"
    ]
  }
]


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
offset	
Allow an offset parameter to specify the start in the history to get events from. Defaults to 0

query	double
count	
Allow a count parameter to specify the number of events to get from the log. Defaults to 50

query	double
type_id	
Allows the user to filter events by type

query	double
post /history/events
Parameters
Parameter	Value	Description	Parameter Type	Data Type
type_id	
(required)
formData	double
parameters	
Provide multiple values in new lines (at least one required).
formData	Array[string]
Response Messages
HTTP Status Code	Reason	Response Model	Headers
200	
Event logged

400	
Bad request, some input value was not excepted.

Camera : Camera image and videoShow/HideList OperationsExpand Operations
get /camera
Implementation Notes
Returns camera object

Response Class (Status 200)
Camera object

ModelExample Value
{
  "feed": "string"
}


Response Content Type 
application/json
get /camera/feed
Implementation Notes
Get a link to the camera feed, this returns an url to a camera stream

Response Class (Status 200)
string


Response Content Type 
application/json
get /camera/{index}/stream
Implementation Notes
Get a redirection to the camera live feed.

Parameters
Parameter	Value	Description	Parameter Type	Data Type
index	
(required)
index of the camera to get the feed from.

path	double
Response Messages
HTTP Status Code	Reason	Response Model	Headers
302	
Redirection to the camera feed.

404	
Camera with this index is not available in the system.

get /camera/{index}/snapshot
Implementation Notes
Get a redirection to the camera snapshot.

Parameters
Parameter	Value	Description	Parameter Type	Data Type
index	
(required)
index of the camera to get the snapshot from.

path	double
Response Messages
HTTP Status Code	Reason	Response Model	Headers
302	
Redirection to the camera snapshot.

404	
Camera with this index is not available in the system.

AirManager : Air-manager peripheralShow/HideList OperationsExpand Operations
get /airmanager
Implementation Notes
Returns Air-manager details

Response Class (Status 200)
Air-manager details

ModelExample Value
{
  "firmware_version": "string",
  "filter_age": 0,
  "filter_max_age": 0,
  "filter_status": "unknown",
  "status": "error",
  "fan_speed": 0
}


Response Content Type 
application/json
Licensing : Premium features and associated licensesShow/HideList OperationsExpand Operations
get /licenses
Response Class (Status 200)
All available premium features on the printer, and their licensing status.

ModelExample Value
{
  "print_process_reporting": "unlicensed"
}


Response Content Type 
application/json
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
This printer does not support premium features.

post /licenses
Response Class (Status 200)
License file installed.

ModelExample Value
[
  "print_process_reporting"
]


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
file	Aucun fichier choisi	
UMLICENSE file

formData	file
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
This printer does not support premium features.

get /licenses/{module_id}
Response Class (Status 200)
License data for this module, if any.

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
module_id	
(required)
ID of the premium module.

path	string
Response Messages
HTTP Status Code	Reason	Response Model	Headers
404	
This printer does not support premium features.

ambient_temperatureShow/HideList OperationsExpand Operations
get /ambient_temperature
Implementation Notes
Returns the ambient temperature

Response Class (Status 200)
Ambient temperature

ModelExample Value
{
  "current": 0
}


Response Content Type 
application/json
