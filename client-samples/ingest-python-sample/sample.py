import argparse
import re
from time import sleep
import polars as pl
from pydozer.ingest import IngestClient
from pydozer.api import ApiClient

DOZER_CLOUD_HOST = "data.dev.getdozer.io:443"


def get_api_client(app_id=None, token=None):
    return ApiClient("trips", url=DOZER_CLOUD_HOST, app_id=app_id,
                     secure=True, token=token) if app_id else ApiClient("trips", url="localhost:80")


def get_ingest_client(app_id=None):
    return IngestClient(url=DOZER_CLOUD_HOST, app_id=app_id,
                        secure=True) if app_id else IngestClient(url="localhost:80")


def main(app_id=None, token=None):

    ingest_client = get_ingest_client(app_id)
    df = pl.read_parquet('data/trips/fhvhv_tripdata_2022-01.parquet')
    small = df.head(2000)
    ingest_client.ingest_df_arrow("trips", small)

    sleep(1)

    api_client = get_api_client(app_id, token)
    # Get Record Count
    trips_count = api_client.count()
    print(trips_count)

    # Query with $limit, $filter and $order_by
    trips = api_client.query({'$limit': 1})
    if trips and trips.records:
        print(trips.records[0])
    else:
        print("No records found")


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-a", "--app", help="The Application id")
    argParser.add_argument("-t", "--token", help="API Token")
    args = argParser.parse_args()

    main(args.app, args.token)