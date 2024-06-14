## Nested Dozer Connector

Dozer can be launched as multiple distributed micro services. 
This example demonstrates connecting to another downstream dozer application. 

## Steps

1) Follow the instructions at  [local-storage](../local-storage/README.md) and run local-storage. 
```bash
# Initialize the dataset
cd ../local-storage
dozer

.____   ___ __________ ____
|  _ \ / _ \__  / ____|  _ \
| | | | | | |/ /|  _| | |_) |
| |_| | |_| / /_| |___|  _ <
|____/ \___/____|_____|_| \_\


Dozer Version: 0.1.31

 INFO Initiating app: local-storage-sample
```

2) Run nested dozer in the nested directory  

```bash
dozer


.____   ___ __________ ____
|  _ \ / _ \__  / ____|  _ \
| | | | | | |/ /|  _| | |_) |
| |_| | |_| / /_| |___|  _ <
|____/ \___/____|_____|_| \_\


Dozer Version: 0.1.31

 INFO Initiating app: nested-trips
```

Now you have two dozer apps runnings

`local-storage-sample` exposing rest API on 8080 and gRPC on 50051

```bash
curl localhost:8080/trips
```

`nested-trips` exposing rest API on 7002 and gRPC on 7003

```bash
 curl localhost:7002/nested_trips
```