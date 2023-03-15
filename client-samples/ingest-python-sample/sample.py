
from time import sleep
import polars as pl
from dozer.ingest import IngestClient
from dozer.api import ApiClient

df = pl.read_parquet('data/trips/fhvhv_tripdata_2022-01.parquet')
ingest_client = IngestClient(url="localhost:7005")
small = df.head(1000)
ingest_client.ingest_df_arrow("trips", small)

sleep(1)

api_client = ApiClient("trips", url="localhost:7003")
# Get Record Count
trips_count = api_client.count()
print(trips_count)

# Query with $limit, $filter and $order_by
trips = api_client.query({'$limit': 1})
if trips and trips.records:
  print(trips.records[0])
else:
  print("No records found")
