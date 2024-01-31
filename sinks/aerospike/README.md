
# Postgres to Aerospike


## Requirements
- Postgres
- Aerospike


Run Postgres
```bash
docker run --name some-postgres -e POSTGRES_PASSWORD=postgres -d postgres

# Import chinook
psql -h 127.0.0.1 -U postgres < ./data/chinook_db.sql

```

Run Aerospike
```bash
docker run -d --name aerospike -p 3000-3002:3000-3002 aerospike:ee-7.0.0.3
```

AQL
```bash
docker run -it aerospike/aerospike-tools aql -h  $(docker inspect -f '{{.NetworkSettings.IPAddress}}' aerospike)
```
