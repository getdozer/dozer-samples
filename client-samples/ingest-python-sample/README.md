## Dataframe / Arrow Ingestion Example

This example shows how to ingest dataframes in arrow format into Dozer and readily serve APIs.

## Dependencies
 - [poetry](https://python-poetry.org/docs/)
 
## Initialization
Refer to [Installation](https://getdozer.io/docs/installation) for instructions.

Download the sample dataset from [NYC - TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
```bash
./init.sh
```

You can refer to the full example in this [notebook](./sample.ipynb)
### Run Dozer in one terminal
```bash
dozer
```

### Ingest data
```python
import polars as pl
from pydozer.ingest import IngestClient

df = pl.read_parquet('data/trips/fhvhv_tripdata_2022-01.parquet')
ingest_client = IngestClient(url="localhost:7005")
small = df.head(1000)
ingest_client.ingest_df_arrow("trips", small)
```


### Sample Queries

```python
from pydozer.api import ApiClient

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

```
