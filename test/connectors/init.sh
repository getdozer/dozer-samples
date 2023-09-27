#!/bin/sh
BASEDIR=$(dirname "$0")
cd ${BASEDIR}/../../

mkdir -p ./connectors/local-storage/data/trips
cp ./test/fixtures/small_trips.parquet ./connectors/local-storage/data/trips/small_trips.parquet
