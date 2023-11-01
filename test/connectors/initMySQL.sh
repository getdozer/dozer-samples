#!/bin/sh
BASEDIR=$(dirname "$0")
cd ${BASEDIR}/../../

docker-compose -f ./connectors/mysql/docker-compose.yml up -d