#IMDB - Analytics

## Prerequisites

- [Dozer] (https://getdozer.io/docs/getting_started)
- MySQL
- Docker
- Cargo

## Download the .sql file

```bash

```

## Start prometheus server

```bash
docker compose up
```

## Start the dashboard UI (Optional)

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
dozer clean -c aggregate-config.yaml
dozer build -c aggregate-config.yaml
dozer run app -c aggregate-config.yaml
```