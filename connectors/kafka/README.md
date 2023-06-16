# Running Redpanda, Producer, and Dozer

This readme provides step-by-step instructions on running Redpanda, a producer for generating sample data, and Dozer for ingesting the Redpanda data and querying it. By following these steps, you will have a local setup where you can produce and consume data using Redpanda and Dozer.

## Prerequisites

Before starting, ensure that you have the following installed:

- Docker
- Python 3.9 or above
- Dozer

## Setup Instructions

### Step 1: Run Redpanda

1. Create a file named `docker-compose.yaml` with the contents present in [`docker-compose.yml`](docker-compose.yml) from the repo:

2. Run the following command to start Redpanda:

```bash
docker-compose up -d
```

### Step 2: Register Schema

To enable schema validation for the transaction data, you need to register the schema with the Schema Registry.

Run the following command to register the transaction schema:

```bash
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" --data '{"schema": "{\"type\":\"record\",\"name\":\"transaction\",\"namespace\":\"dozer.samples\",\"fields\":[{\"name\":\"id\",\"type\":\"int\"}, {\"name\":\"customer_id\",\"type\":\"int\"},{\"name\":\"amount\",\"type\":\"float\"},{\"name\":\"location\",\"type\":\"string\"},{\"name\":\"provider\",\"type\":\"string\"}]}"}' http://localhost:18081/subjects/transactions-value/versions


curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" --data '{"schema": "{\"type\":\"record\",\"name\":\"transactions\",\"namespace\":\"dozer.samples\",\"fields\":[{\"name\":\"id\",\"type\":\"int\"}]}"}' http://localhost:18081/subjects/transactions-key/versions
```

### Step 3: Run the Producer

1. Create a Python script named `producer.py` with the code to generate sample data and publish it to Redpanda or use [`producer.py`](producer.py) from the repo

2. Run the following command to start the producer:

```bash
python producer.py
```

The producer will start generating sample data and publish it to Redpanda.

### Step 4: Run Dozer

1. Create a configuration file named `dozer-config.yaml` with the necessary configuration for Dozer. You can use the same [`dozer-config.yaml`](dozer-config.yaml) from this repo as well.

2. Run the following command to start Dozer:

```bash
dozer -c dozer-config.yaml
```

Dozer will ingest the data from Redpanda and perform the specified operations based on the configuration.

### Step 5: Querying Dozer

1. Once Dozer is running, you can query the ingested data.

2. Use the specified endpoints or methods provided by Dozer to access the ingested data and perform queries as needed.
