# Scaling E-Commerce

## Prerequisites

- [Dozer](https://getdozer.io/docs/getting_started)
- JRE
- Docker
- Yarn
- Cargo

## Generate dataset

```bash
poetry install
poetry shell
python generate.py
```

## Start prometheus server

```bash
docker compose up
```

## Start the dashboard UI (Optional)

```bash
docker-compose up
```
> Note: For linux users, change the network mode to `host` and update prometheus config to `localhost:9000`

## Run dozer

Follow the instructions here and install [Dozer](https://getdozer.io/docs/getting_started)

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

Once dozer starts running, you should be able to visit the dashboard UI at <http://localhost:3000>.

