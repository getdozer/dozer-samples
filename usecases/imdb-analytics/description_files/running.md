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

## Start the dashboard UI

```bash
docker-compose up
```

## Run dozer

Experiment1: [No ops](./experiment1.md) 

Experiment2: [Single JOIN](./experiment2.md) 

Experiment3: [Multiple JOINs](./experiment3.md) 

Experiment4: [CTE & JOIN](./experiment4.md) 

Experiment5: [Multiple ops](./experiment5.md) 
 
Once dozer starts running, you should be able to visit the dashboard UI at <http://localhost:3000>.