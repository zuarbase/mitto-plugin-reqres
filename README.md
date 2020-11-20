# Mitto Plugin for ReqRes  
  
Example plugin for Mitto (version at the time of publishing was 2.8.7).

This Mitto plugin uses minimal code. It does not create a plugin wizard or have 100% test coverage, etc. It is a very simple example of a Mitto plugin that can be used to create IO jobs that pipe data from a REST API.
  
Create a Mitto `io` job with the job config below to pipe data from the ReqRes `users` endpoint (https://reqres.in/api/users) and store it in Mitto's PostgreSQL database:
```json
{
    "input": {
        "endpoint": "users",
        "use": "reqres.iov2#ReqResInput"
    },
    "output": {
        "dbo": "postgresql://localhost/analytics",
        "schema": "reqres",
        "tablename": "users",
        "use": "call:mitto.iov2.db#todb"
    },
    "steps": [
        {
            "transforms": [
                {
                    "use": "mitto.iov2.transform#ExtraColumnsTransform"
                },
                {
                    "use": "mitto.iov2.transform#ColumnsTransform"
                }
            ],
            "use": "mitto.iov2.steps#Input"
        },
        {
            "use": "mitto.iov2.steps#CreateTable"
        },
        {
            "transforms": [
                {
                    "use": "mitto.iov2.transform#FlattenTransform"
                }
            ],
            "use": "mitto.iov2.steps#Output"
        },
        {
            "use": "mitto.iov2.steps#CollectMeta"
        }
    ]
}
```

Duplicate the Mitto job above and update the `input` `endpoint` and `output` `tablename` to pipe data from the Reqres `unknown` endpoint (https://reqres.in/api/unknown) and store it in Mitto's PostgreSQL database:
```json
{
    "input": {
        "endpoint": "unknown",
        "use": "reqres.iov2#ReqResInput"
    },
    "output": {
        "dbo": "postgresql://localhost/analytics",
        "schema": "reqres",
        "tablename": "unknown",
        "use": "call:mitto.iov2.db#todb"
    },
    "steps": [
        {
            "transforms": [
                {
                    "use": "mitto.iov2.transform#ExtraColumnsTransform"
                },
                {
                    "use": "mitto.iov2.transform#ColumnsTransform"
                }
            ],
            "use": "mitto.iov2.steps#Input"
        },
        {
            "use": "mitto.iov2.steps#CreateTable"
        },
        {
            "transforms": [
                {
                    "use": "mitto.iov2.transform#FlattenTransform"
                }
            ],
            "use": "mitto.iov2.steps#Output"
        },
        {
            "use": "mitto.iov2.steps#CollectMeta"
        }
    ]
}
```

This plugin has not been tested on any other endpoints. 