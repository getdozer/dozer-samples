## Dozer MySQL Starter

## Initialization
Refer to [Installation](https://getdozer.io/docs/installation) for instructions.

## Running

Run a sample MySQL database on the port `3306`
```bash
docker compose up
```

Running Dozer
```bash

export MYSQL_URL="mysql://root:mysql@localhost:3306/Chinook"

dozer
```

That's all to it. You have APIs instantly available over REST and gRPC.

```

.____   ___ __________ ____
|  _ \ / _ \__  / ____|  _ \
| | | | | | |/ /|  _| | |_) |
| |_| | |_| / /_| |___|  _ <
|____/ \___/____|_____|_| \_\


Dozer Version: 0.1.34

 INFO Initiating app: dozer-chinook-mysql
 INFO Home dir: ./.dozer
 INFO [API] Endpoints
+-----------+----------+
| Path      | Name     |
+-----------+----------+
| /employee | employee |
+-----------+----------+
| /invoice  | invoice  |
+-----------+----------+

 INFO Source: Initializing input schema: Invoice
+-------------+-----------+----------+-------+
| Field       | Type      | Nullable | PK    |
+-------------+-----------+----------+-------+
| InvoiceId   | Int       | false    | true  |
+-------------+-----------+----------+-------+
| CustomerId  | Int       | false    | false |
+-------------+-----------+----------+-------+
| InvoiceDate | Timestamp | false    | false |
+-------------+-----------+----------+-------+
| Total       | Decimal   | false    | false |
+-------------+-----------+----------+-------+

 INFO Source: Initializing input schema: Employee
+------------+-----------+----------+-------+
| Field      | Type      | Nullable | PK    |
+------------+-----------+----------+-------+
| EmployeeId | Int       | false    | true  |
+------------+-----------+----------+-------+
| LastName   | Text      | false    | false |
+------------+-----------+----------+-------+
| FirstName  | Text      | false    | false |
+------------+-----------+----------+-------+
| Title      | Text      | true     | false |
+------------+-----------+----------+-------+
| ReportsTo  | Int       | true     | false |
+------------+-----------+----------+-------+
| BirthDate  | Timestamp | true     | false |
+------------+-----------+----------+-------+
| HireDate   | Timestamp | true     | false |
+------------+-----------+----------+-------+
| Address    | Text      | true     | false |
+------------+-----------+----------+-------+
| City       | Text      | true     | false |
+------------+-----------+----------+-------+
| State      | Text      | true     | false |
+------------+-----------+----------+-------+
| Country    | Text      | true     | false |
+------------+-----------+----------+-------+
| PostalCode | Text      | true     | false |
+------------+-----------+----------+-------+
| Phone      | Text      | true     | false |
+------------+-----------+----------+-------+
| Fax        | Text      | true     | false |
+------------+-----------+----------+-------+
| Email      | Text      | true     | false |
+------------+-----------+----------+-------+

 INFO [pipeline] Validation completed
 INFO Created new build v0001
 INFO Source: Initializing input schema: Invoice
+-------------+-----------+----------+-------+
| Field       | Type      | Nullable | PK    |
+-------------+-----------+----------+-------+
| InvoiceId   | Int       | false    | true  |
+-------------+-----------+----------+-------+
| CustomerId  | Int       | false    | false |
+-------------+-----------+----------+-------+
| InvoiceDate | Timestamp | false    | false |
+-------------+-----------+----------+-------+
| Total       | Decimal   | false    | false |
+-------------+-----------+----------+-------+

 INFO Source: Initializing input schema: Employee
+------------+-----------+----------+-------+
| Field      | Type      | Nullable | PK    |
+------------+-----------+----------+-------+
| EmployeeId | Int       | false    | true  |
+------------+-----------+----------+-------+
| LastName   | Text      | false    | false |
+------------+-----------+----------+-------+
| FirstName  | Text      | false    | false |
+------------+-----------+----------+-------+
| Title      | Text      | true     | false |
+------------+-----------+----------+-------+
| ReportsTo  | Int       | true     | false |
+------------+-----------+----------+-------+
| BirthDate  | Timestamp | true     | false |
+------------+-----------+----------+-------+
| HireDate   | Timestamp | true     | false |
+------------+-----------+----------+-------+
| Address    | Text      | true     | false |
+------------+-----------+----------+-------+
| City       | Text      | true     | false |
+------------+-----------+----------+-------+
| State      | Text      | true     | false |
+------------+-----------+----------+-------+
| Country    | Text      | true     | false |
+------------+-----------+----------+-------+
| PostalCode | Text      | true     | false |
+------------+-----------+----------+-------+
| Phone      | Text      | true     | false |
+------------+-----------+----------+-------+
| Fax        | Text      | true     | false |
+------------+-----------+----------+-------+
| Email      | Text      | true     | false |
+------------+-----------+----------+-------+

 INFO [pipeline] Validation completed
 INFO Starting Internal Server on 0.0.0.0:50053
 INFO Starting Rest Api Server on http://0.0.0.0:8080 with security: None
 INFO starting 8 workers
 INFO Tokio runtime found; starting in existing Tokio runtime
 INFO Starting gRPC server on 0.0.0.0:50051 with security: None
```


### Querying Dozer

**REST**

Filter with limit of 3
```bash
curl -X POST  http://localhost:8080/invoice/query \
--header 'Content-Type: application/json' \
--data-raw '{"$limit":3}'
```

```json
[
  {
    "InvoiceId": 1,
    "CustomerId": 2,
    "InvoiceDate": "2009-01-01T00:00:00.000Z",
    "Total": "1.98",
    "__dozer_record_id": 0,
    "__dozer_record_version": 1
  },
  {
    "InvoiceId": 2,
    "CustomerId": 4,
    "InvoiceDate": "2009-01-02T00:00:00.000Z",
    "Total": "3.96",
    "__dozer_record_id": 1,
    "__dozer_record_version": 1
  },
  {
    "InvoiceId": 3,
    "CustomerId": 8,
    "InvoiceDate": "2009-01-03T00:00:00.000Z",
    "Total": "5.94",
    "__dozer_record_id": 2,
    "__dozer_record_version": 1
  }
]
```

For more about REST in Dozer, see [Using REST APIs](https://getdozer.io/docs/querying/rest).

**`gRPC`**
Filter with limit of 1
```
grpcurl -d '{"query": "{\"$limit\": 1}"}' \
-plaintext localhost:50051 \
dozer.generated.invoice.Invoices/query
```
Response
```
{
  "records": [
    {
      "record": {
        "InvoiceId": "1",
        "CustomerId": "2",
        "InvoiceDate": "2009-01-01T00:00:00Z",
        "Total": {
          "scale": 2,
          "lo": 198
        },
        "DozerRecordVersion": 1
      }
    }
  ]
}
```

For more about gRPC in Dozer, see [Using gRPC APIs](https://getdozer.io/docs/querying/grpc).

## Dozer Cloud

1. Setup MYSQL database on EC2 Instance using docker compose in dozer-cloud-docker folder.
2. Pass in the credentials in the config file
3. Run the following command to deploy the app on Dozer Cloud

```bash
dozer cloud deploy
```

### Deploy with environment variables

```bash
 dozer cloud deploy -s EC2_INSTANCE_DNS=$EC2_INSTANCE_DNS 
 ```


##  Query data on cloud

```bash
curl -H "X-Dozer-App-Id: <app-id" -H "Authorization: Bearer <bearer-token>" https://dataW.getdozer.io:443
```
