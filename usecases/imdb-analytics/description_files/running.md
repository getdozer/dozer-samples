#IMDB - Analytics

## Prerequisites

- [Dozer](https://getdozer.io/docs/getting_started)
- MySQL
- Docker
- Cargo

## Download the .sql file and insert it into a database IMDB

This step will take time depending upon the insertion speed for MySQL, the speed can be improved by increasing the `innodb_buffer_pool_size` of MySQL.

```bash
#Download the .sql file
bash init.sh
#Insert data into a database IMDB in MySQL
mysql -u <username> -p IMDB < imdb_data.sql
```

## Run dozer

Experiment1: [No ops](./experiment1.md) 

Experiment2: [Double JOIN](./experiment2.md) 

Experiment3: [ JOINs & CTEs](./experiment3.md) 

Experiment4: [CTE & JOIN](./experiment4.md) 

## Start dozer live (Optional)

Note: Dozer live will not be able to start a new instance unless you stop previous instances of Dozer.

```bash
dozer live -c <config-file>
```

eg. to run experiment1

```bash
dozer live -c exp1-config.yaml
```