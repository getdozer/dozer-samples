# A guide to using Dozer SQL

This is a comprehensive guide showcasing different types of queries possible with Dozer SQL.

## Dataset 

We will be using two tables throughout this guide. These tables are from [NYC - TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). To download these run the command,

```bash
bash download.sh
```

### Table 1: trips

This table is contained in a parquet file under `data/trips/yellow_tripdata_2022-01.parquet`.

![table_1_image](/sql/images/table_1.png)


### Table 2: taxi_zone_lookup 

This table is contained in a csv file under `data/zones/taxi_zone_lookup.csv`.

![table_2_image](/sql/images/table_2.png)

These tables can be joined based on the `LocationID`.

## Basics

Since Dozer fetches data from sources, and puts it out at the endpoints therefore it is crucial for every Dozer SQL statement to have a top-level `SELECT` clause as well as atleast one `FROM` clause.

These are pretty standard rules for a normal retrieve statement in SQL, however, Dozer SQL also requires the use of an `INTO` clause. This will specify the name of the table that the endpoints will use to fetch the data from.

Hence, the basic statement structure is,

```sql
 SELECT A INTO C FROM B;
```
The datatypes and casting compatible with Dozer SQL is described in the [documentation for datatypes and casting](https://getdozer.io/docs/transforming-data/data-types).

Dozer SQL supports primitive scalar function described in [documentation for scalar functions](https://getdozer.io/docs/transforming-data/scalar-functions).


## Table of contents

Let us start with basic Dozer SQL queries and move towards more complex queries. 

| Sr.no | Query type | Description                                                          |
| ----- | ---------- | -------------------------------------------------------------------- |
|   1   |   [Filtering](./filtering/README.md)    |  A simple select operation with a `WHERE` clause  |
|   2   |   [Aggregation](./aggregation/README.md)   |  Multiple queries each describing a specifc aggregation on the data  |
|   3   |   [JOIN](./join/README.md)   |  Query to JOIN the tables based on `LocationID` |
|   4   |   [CTEs](./cte/README.md)   |  Query with two CTE tables JOINed after filtering |
|   5   |   [Sub queries](./sub-queries/README.md)   |  Multiple queries describing nested `SELECT` statements |
|   6   |   [Window functions](./window-functions/README.md)   |  Queries describing the use of `TUMBLE` and `HOP` |

## Running


### Dozer

To run Dozer navigate to the folder with the configuration you want to run, and use the command,

```bash
dozer run
```

To remove the cache directory, use

```bash
dozer clean
```


### Dozer Live

To run with Dozer live, replace `run` with `live`

```bash
dozer live
```

Dozer live automatically deletes the cache upon stopping the program.