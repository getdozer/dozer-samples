## Step 1: Set Up Ethereum environment

Download following file into your current working directory.

Get a websocket url from one of the hosted eth node providers such as [Infura](https://www.infura.io/product/ethereum) and initialize the env variable `ETH_WSS_URL`.


```bash
# Intialize ETH Web Socker Url
export ETH_WSS_URL=<WSS_URL>
```

## Step 2: Build Dozer from source for enabling Ethereum

```bash
cargo build --bin dozer --features ethereum --release
```


## Step 3: Run Dozer


```bash
./dozer -c dozer-config.yml
```


That's all to it. You have APIs instantly available over REST and gRPC.

```

____   ___ __________ ____
|  _ \ / _ \__  / ____|  _ \
| | | | | | |/ /|  _| | |_) |
| |_| | |_| / /_| |___|  _ <
|____/ \___/____|_____|_| \_\


Dozer Version: 0.1.21

2023-05-12T10:09:20.046054Z  INFO Starting Rest Api Server on http://0.0.0.0:8080 with security: None
2023-05-12T10:09:20.046217Z  INFO Starting gRPC server on http://0.0.0.0:50051 with security: None
```


### Querying Dozer

**Using REST**:

Filter with limit of 3
```
curl -X POST  http://localhost:8080/transfers/query \
--header 'Content-Type: application/json' \
--data-raw '{"$limit":3}'

[
  {
    "from": "0xdbfd76af2157dc15ee4e57f3f942bb45ba84af24",
    "to": "0xdafce4acc2703a24f29d1321adaadf5768f54642",
    "__dozer_record_id": 0,
    "__dozer_record_version": 1
  },
  {
    "from": "0xdafce4acc2703a24f29d1321adaadf5768f54642",
    "to": "0x47dc79cdd0c878ffc190f9838af30a3c63a21a9b",
    "__dozer_record_id": 1,
    "__dozer_record_version": 1
  },
  {
    "from": "0x47dc79cdd0c878ffc190f9838af30a3c63a21a9b",
    "to": "0xdafce4acc2703a24f29d1321adaadf5768f54642",
    "__dozer_record_id": 2,
    "__dozer_record_version": 1
  }
]```
