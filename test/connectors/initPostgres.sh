#!/bin/sh
BASEDIR=$(dirname "$0")
cd ${BASEDIR}/../../connectors/postgres

sh download.sh

docker-compose up -d