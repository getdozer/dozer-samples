## Scaling E-Commerce

In this example we demonstrate Dozer's capability of processing large volume of data. This is mainly focused on processing performance. API performance will be published separately. 

## Table of Contents
- [Scaling E-Commerce](#scaling-e-commerce)
- [Table of Contents](#table-of-contents)
- [Data Schema and Volume](#data-schema-and-volume)
- [Instance Type](#instance-type)
- [Experiment 1](#experiment-1)
  - [Instructions](#instructions)
  - [Findings](#findings)
- [Experiment 2](#experiment-2)
  - [Instructions](#instructions-1)
  - [Findings](#findings-1)
- [API Performance](#api-performance)
  - [Instructions](#instructions-2)
  - [Findings](#findings-2)

Running instructions can be [found here](./running.md)
## Data Schema and Volume

Let's consider the following schema. The data source has 4 tables: `orders`, `order_items`, `products`, `customers`. 

![Schema](./images/schema.png)

Data has been generated using `dbldatagen`. 
We generate 11 million rows for customers, 11 million rows for orders, 10 million rows for products, and 100 million rows for order_items. These parameters can be adjusted in [`generate.py`](./generate.py).

| Table       | No of Rows  |
| ----------- | ----------- |
| customers   | 11_000_000  |
| orders      | 11_000_000  |
| order_items | 100_000_000 |
| products    | 16_000_000  |


## Instance Type

Following tests have been run on AWS Graviton `m7g.8xlarge` type. Potentially storage optimized instances such as `im4gn.large` could be used if high amount of disk reads are to be expected in the case of external storage. 

| Instance Type | vCPUs | Memory(Gb) |
| ------------- | ----- | ---------- |
| m7g.8xlarge   | 32    | 128        |



## Experiment 1

Running `dozer` direct from `source` to `cache`.

### Instructions
```
dozer clean -c direct-config.yaml
dozer build -c direct-config.yaml
dozer run app -c direct-config.yaml
```

### Findings

![Experiement 1](./images/experiment_1.png)

 - Roughly took `4 mins` to process all the records. 
 - Note that processing of `customers`, `orders` and `order_items` finished in about `2 mins` compared to `products`.
 - Pipeline latency is very low (`~0.04`) as there is no transformation involved.
 
| Start Time | End Time   | Elapsed  |
| ---------- | ---------- | -------- |
| 3:00:50 PM | 3:04:38 PM | ~ 4 mins |


## Experiment 2

Running `dozer` with aggregations and joins.

We run 3 cascading JOINs and a COUNT aggregation on the data source. The sql can be found in [`aggregate-config.yaml`](./aggregate-config.yaml).

```sql
select c.customer_id, c.name, c.email,  o.order_id, o.order_date, o.total_amount, COUNT(*)
  into customer_orders 
  from customers c
  inner join orders o on c.customer_id = o.customer_id
  join order_items i on o.order_id = i.order_id
  join products p on i.product_id = p.product_id
  group by c.customer_id, c.name, c.email, o.order_id, o.order_date, o.total_amount
```

### Instructions
```
dozer clean -c aggregate-config.yaml
dozer build -c aggregate-config.yaml
dozer run app -c aggregate-config.yaml
```


### Findings

![Experiement 2](./images/experiment_2.png)

 - Roughly took `12 mins` to process all the records. 
 - Note that here total number of `order_items` increases in conjunction with `products`. This is to due to the dependency of the join. 
 - Pipeline latency stays under `1s` even with 4 joins and an aggregation.
 
| Start Time | End Time   | Elapsed   |
| ---------- | ---------- | --------- |
| 2:32:48 PM | 2:44:51 PM | ~ 12 mins |


## API Performance

Dozer really shines when it comes to API performance as views are pre-materialized.
Dozer automatically generates `gRPC` and `REST`  APIs.

Lets use `ghz` to run a loadtest against the `gRPC` server. You can find the [script here](./load_test_grpc.sh)

### Instructions
```bash
`HOST=localhost:50051
TOTAL=1000000
CONCURRENCY=50
echo "Testing common grpc service with $TOTAL requests and $CONCURRENCY concurrency"
ghz --insecure --proto ./dozer-api/protos/common.proto --call dozer.common.CommonGrpcService.query --total $TOTAL --concurrency $CONCURRENCY --data '{"endpoint":"customers"}' $HOST`
```

### Findings

Dozer maintains an average of `4.92 ms` at a very high throughput of `10000` total requests at `50` concurrency.

```bash
Summary:
  Count:	100000
  Total:	10.83 s
  Slowest:	30.56 ms
  Fastest:	1.27 ms
  Average:	4.92 ms
  Requests/sec:	9234.20

Response time histogram:
  1.268  [1]     |
  4.197  [48567] |∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  7.126  [36274] |∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  10.056 [10248] |∎∎∎∎∎∎∎∎
  12.985 [3135]  |∎∎∎
  15.915 [1152]  |∎
  18.844 [414]   |
  21.773 [104]   |
  24.703 [73]    |
  27.632 [26]    |
  30.561 [6]     |

Latency distribution:
  10 % in 2.44 ms
  25 % in 3.18 ms
  50 % in 4.27 ms
  75 % in 5.92 ms
  90 % in 8.11 ms
  95 % in 10.00 ms
  99 % in 14.63 ms

Status code distribution:
  [OK]   100000 responses
```