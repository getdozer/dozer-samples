## IMDB - Analytics

In this example we demonstrate Dozer's capabilities to find meaningful insights by processing large amounts of data.

## Data Schema and Volume

The dataset used here is taken from [CMU 15-445/645 Coursework](https://15445.courses.cs.cmu.edu/fall2022/homework1/) which also has many examples of interesting SQL queries.

For this example we are loading the data into a MySQL database. Steps to do the same can be found [here](./running.md).

![Schema](./images/schema.png)

 The dataset has six tables: `akas` , `crew` , `episodes` , `people` , `ratings` , `title`, with roughly 17 million data records in total.

| Table       | No of Rows  |
| ----------- | ----------- |
| akas        | 4_947_919   |
| crew        | 7_665_208   |
| episodes    |  157_869    |
| people      | 1_782_303   |
| ratings     |  188_159    |
| title       | 1_375_462   |

## Hardware Configuration

|      CPU       | Cores |   Memory   |     Storage       |
| -------------- | ----- | ---------- | ----------------- |
| Ryzen7 4800H   |  16   |    16GB    |  200GB NVMe SSD   |

## Experiment 1

Running `dozer` direct from `source` to `cache`.

## Instructions
```
dozer clean -c direct-config.yaml
dozer build -c direct-config.yaml
dozer run app -c direct-config.yaml
```

![Experiement 1](./images/experiment_1.png)

 - Roughly took `4 mins` to process all the records. 
 - Note that processing of `customers`, `orders` and `order_items` finished in about `2 mins` compared to `products`.
 - Pipeline latency is very low (`~0.04`) as there is no transformation involved.

| Start Time | End Time   | Elapsed  |
| ---------- | ---------- | -------- |
| 3:00:50 PM | 3:04:38 PM | ~ 4 mins |