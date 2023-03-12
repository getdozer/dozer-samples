## SQL Aggregation example

This example shows how to use SQL aggregation in Dozer

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
curl -X POST  http://localhost:8080/total_distance/query \
--header 'Content-Type: application/json' \
--data-raw '{"$limit":3}'
```

```
[
    {"vendor":6,"total_distance":45929.08,"__dozer_record_id":2,"__dozer_record_version":5563},
    {"vendor":5,"total_distance":536.8,"__dozer_record_id":3,"__dozer_record_version":36},
    {"vendor":2,"total_distance":10974248.94,"__dozer_record_id":1,"__dozer_record_version":1716059}
]
```

