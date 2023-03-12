## SQL WINDOW functions example

This example shows how to apply WINDOW functions to a source in Dozer

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

Get the result for tumble window
```
curl -X POST  http://localhost:8080/tumble/query \
--header 'Content-Type: application/json' \
--data-raw '{"$limit":5}'
```

```
[
    {"location":142,"pickup_time":"2022-01-01T00:35:40.000Z","start":"2022-01-01T00:35:00.000Z","end":"2022-01-01T00:40:00.000Z","__dozer_record_id":0,"__dozer_record_version":1},
    {"location":132,"pickup_time":"2022-01-02T05:34:05.000Z","start":"2022-01-02T05:30:00.000Z","end":"2022-01-02T05:35:00.000Z","__dozer_record_id":65536,"__dozer_record_version":1},
    {"location":43,"pickup_time":"2022-01-03T09:45:59.000Z","start":"2022-01-03T09:45:00.000Z","end":"2022-01-03T09:50:00.000Z","__dozer_record_id":131072,"__dozer_record_version":1},
    {"location":262,"pickup_time":"2022-01-04T08:52:31.000Z","start":"2022-01-04T08:50:00.000Z","end":"2022-01-04T08:55:00.000Z","__dozer_record_id":196608,"__dozer_record_version":1},
    {"location":113,"pickup_time":"2022-01-04T23:02:57.000Z","start":"2022-01-04T23:00:00.000Z","end":"2022-01-04T23:05:00.000Z","__dozer_record_id":262144,"__dozer_record_version":1}
]
```

Get the result for hop window
```
curl -X POST  http://localhost:8080/hop/query \
--header 'Content-Type: application/json' \
--data-raw '{"$limit":5}'
```

```
[
    {"location":142,"pickup_time":"2022-01-01T00:35:40.000Z","start":"2022-01-01T00:34:00.000Z","end":"2022-01-01T00:36:00.000Z","__dozer_record_id":0,"__dozer_record_version":1},
    {"location":246,"pickup_time":"2022-01-01T14:47:53.000Z","start":"2022-01-01T14:46:00.000Z","end":"2022-01-01T14:48:00.000Z","__dozer_record_id":65536,"__dozer_record_version":1},
    {"location":132,"pickup_time":"2022-01-02T05:34:05.000Z","start":"2022-01-02T05:33:00.000Z","end":"2022-01-02T05:35:00.000Z","__dozer_record_id":131072,"__dozer_record_version":1},
    {"location":24,"pickup_time":"2022-01-02T17:31:18.000Z","start":"2022-01-02T17:30:00.000Z","end":"2022-01-02T17:32:00.000Z","__dozer_record_id":196608,"__dozer_record_version":1},
    {"location":43,"pickup_time":"2022-01-03T09:45:59.000Z","start":"2022-01-03T09:44:00.000Z","end":"2022-01-03T09:46:00.000Z","__dozer_record_id":262144,"__dozer_record_version":1}
]
```


**`gRPC`**

Filter with limit of 1
```
grpcurl -d '{"query": "{\"$limit\": 1}"}' \
-plaintext localhost:50051 \
dozer.generated.tumble.Tumbles/query
```
Response
```
{
  "records": [
    {
      "record": {
        "location": "142",
        "pickupTime": "2022-01-01T00:35:40Z",
        "start": "2022-01-01T00:35:00Z",
        "end": "2022-01-01T00:40:00Z",
        "DozerRecordVersion": 1
      }
    }
  ]
}
```


 

