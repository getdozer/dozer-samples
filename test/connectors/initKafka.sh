#!/bin/sh
BASEDIR=$(dirname "$0")
cd ${BASEDIR}/../../connectors/kafka

#start RedPanda
docker-compose up -d  

#Register schema
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" --data '{"schema": "{\"type\":\"record\",\"name\":\"transaction\",\"namespace\":\"dozer.samples\",\"fields\":[{\"name\":\"id\",\"type\":\"int\"}, {\"name\":\"customer_id\",\"type\":\"int\"},{\"name\":\"amount\",\"type\":\"float\"},{\"name\":\"location\",\"type\":\"string\"},{\"name\":\"provider\",\"type\":\"string\"}]}"}' http://localhost:18081/subjects/transactions-value/versions


curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" --data '{"schema": "{\"type\":\"record\",\"name\":\"transactions\",\"namespace\":\"dozer.samples\",\"fields\":[{\"name\":\"id\",\"type\":\"int\"}]}"}' http://localhost:18081/subjects/transactions-key/versions

#Run producer script
pip install kafka-python
pip install Faker
python producer.py



