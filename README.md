# Mitto Plugin for ReqRes  
  
Example plugin for Mitto (version at the time of publishing was 2.8.7) which reads users from https://reqres/api/users. It has not been tested on any other endpoints.  
  
Create a Mitto `io` job with the following job config to pull the data into Mitto's PostgreSQL database:
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