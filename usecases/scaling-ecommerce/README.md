# Scaling E-Commerce

In this example we demonstrate Dozer's capability of processing large volume of data.

The data source has 4 tables: `orders`, `order_items`, `products`, `customers`. We run 3 cascading JOINs and a COUNT aggregation on the data source. The sql can be found in [`local-config.yaml`](./local-config.yaml).

We generate 1 million rows for customers, 2 million rows for orders, 400 thousand rows for products, and 10 million rows for order_items. These parameters can be adjusted in [`generate.py`](./generate.py).

## Prerequisites

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

## Start the dashboard UI

Go to <https://github.com/getdozer/dozer-ui> and clone the project.

Go to the `dozer-ui` project directory and run:

```bash
cp .env.lite .env
yarn install
yarn start
```

## Run dozer

First build dozer from source, using code from latest `main`.

Then run dozer with the following command:

```bash
dozer -c local-config.yaml
```

Once dozer starts running, you should be able to visit the dashboard UI at <http://localhost:3000>.

Login to the dashboard with either Github or Google, then you should see metrics like below:

![dozer-ui](./dozer-ui.png)
