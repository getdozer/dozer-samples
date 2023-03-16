## Dozer Snowflake Starter

## Initialization
Install [`Snowflake ODBC`](https://developers.snowflake.com/odbc/)

Reinstall dozer with `snowflake` feature enabled
```bash
cargo install --git https://github.com/getdozer/dozer dozer-orchestrator --locked --features snowflake
```

Copy the sample configuration and edit the environment variables in env.sh
```sh
cp .env.sample.sh cp .env.sh

# Edit the secrets with your Snowflake configuration
source  ./env.sh
```
## Running
Run a dozer with `./dozer-config.yaml`
```
 dozer

____   ___ __________ ____
|  _ \ / _ \__  / ____|  _ \
| | | | | | |/ /|  _| | |_) |
| |_| | |_| / /_| |___|  _ <
|____/ \___/____|_____|_| \_\


Dozer Version: 0.1.11

2023-03-12T10:09:20.046054Z  INFO Starting Rest Api Server on http://0.0.0.0:8080 with security: None
2023-03-12T10:09:20.046217Z  INFO Starting gRPC server on http://0.0.0.0:50051 with security: None
```


### Querying Dozer

**REST**

Filter with limit of 3
```
curl -X POST  http://localhost:8080/films/query \
--header 'Content-Type: application/json' \
--data-raw '{"$limit":3}'
```

```
[
  {"film_id":1,"title":"ACADEMY DINOSAUR","__dozer_record_id":0,"__dozer_record_version":1},
  {"film_id":257,"title":"DRUMLINE CYCLONE","__dozer_record_id":256,"__dozer_record_version":1},
  {"film_id":513,"title":"LEATHERNECKS DWARFS","__dozer_record_id":512,"__dozer_record_version":1}
]
```


**`gRPC`**
Filter with limit of 1
```
grpcurl -d '{"query": "{\"$limit\": 1}"}' \
-plaintext localhost:50051 \
dozer.generated.actors.Actors/query
```
Response
```
{
  "records": [
    {
      "record": {
        "actorId": "1",
        "firstName": "PENELOPE",
        "lastName": "GUINESS",
        "lastUpdate": "2020-02-15T09:34:33Z",
        "DozerRecordVersion": 1
      }
    }
  ]
}
```

Postman

![Postman Actor](./images/actor.png)
