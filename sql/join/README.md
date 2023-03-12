## SQL JOIN example

This example shows how to JOIN two sources with Dozer

## Initialization
Refer to [Installation](https://getdozer.io/docs/installation) for instructions.

Download the sample dataset from [NYC - TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
```bash
./download.sh
```

Running Dozer
```
dozer
```

That's all to it. You have APIs instantly available over REST and gRPC.

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
curl -X POST  http://localhost:8080/pickup/query \
--header 'Content-Type: application/json' \
--data-raw '{"$limit":10}'
```

```
[
    {"pickup_time":"2022-01-01T00:35:40.000Z","zone":"Lincoln Square East","__dozer_record_id":0,"__dozer_record_version":1},
    {"pickup_time":"2022-01-02T05:34:05.000Z","zone":"JFK Airport","__dozer_record_id":65536,"__dozer_record_version":1},
    {"pickup_time":"2022-01-03T09:45:59.000Z","zone":"Central Park","__dozer_record_id":131072,"__dozer_record_version":1},
    {"pickup_time":"2022-01-04T08:52:31.000Z","zone":"Yorkville East","__dozer_record_id":196608,"__dozer_record_version":1},
    {"pickup_time":"2022-01-04T23:02:57.000Z","zone":"Greenwich Village North","__dozer_record_id":262144,"__dozer_record_version":1},
    {"pickup_time":"2022-01-05T20:18:47.000Z","zone":"Gramercy","__dozer_record_id":327680,"__dozer_record_version":1},
    {"pickup_time":"2022-01-06T18:42:39.000Z","zone":"LaGuardia Airport","__dozer_record_id":393216,"__dozer_record_version":1},
    {"pickup_time":"2022-01-07T18:51:43.000Z","zone":"Lenox Hill East","__dozer_record_id":458752,"__dozer_record_version":1},
    {"pickup_time":"2022-01-08T15:36:24.000Z","zone":"Midtown North","__dozer_record_id":524288,"__dozer_record_version":1},
    {"pickup_time":"2022-01-09T12:36:18.000Z","zone":"East Elmhurst","__dozer_record_id":589824,"__dozer_record_version":1}]
```


Postman

![Postman Actor](./images/actor.png)
