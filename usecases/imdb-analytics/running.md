#IMDB - Analytics

## Prerequisites

- [Dozer] (https://getdozer.io/docs/getting_started)
- MySQL
- Docker
- Cargo

## Download the .sql file and insert it into a database IMDB

This step will take time depending upon the insertion speed for MySQL, the speed can be improved by increasing the `innodb_buffer_pool_size` of MySQL.

```bash
bash init.sh
mysql -u <username> -p IMDB < imdb_data.sql
```

## Start the dashboard UI

```bash
docker-compose up
```

## Run dozer

```bash
# Direct from source without transformation
dozer clean -c direct-config.yaml
dozer build -c direct-config.yaml
dozer run app -c direct-config.yaml

# Join and Aggregations
dozer clean -c join-config.yaml
dozer build -c join-config.yaml
dozer run app -c join-config.yaml

# CTEs, Joins and Aggregations
dozer clean -c cte-config.yaml
dozer build -c cte-config.yaml
dozer run app -c cte-config.yaml
```




Once dozer starts running, you should be able to visit the dashboard UI at <http://localhost:3000>.