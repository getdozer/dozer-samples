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


## Run on Dozer Cloud

### Deployment

To deploy the application on Dozer cloud, first login with the cli
```sh
dozer cloud login --organisation_slug <my_organisation_slug> --profile_name <my_profile_name> --client_id <my_dozer_client_id> --client_secret <my_dozer_client_secret>
```

once the login is successful it's possible to deploy the sample application.
```sh
dozer cloud deploy -c dozer-config.yaml -c trips.json
```
Take note of the application id in the logs, it will be referred as `<your_application_id>` in the following commands.

### Ingest Data

The `sample.py` file is a simple python script that ingest a parquet file streaming that to the Dozer gRPC connector.

```sh
python sample.py -a <your_application_id>
```

### Query Data

The `query.py` file is a simple python script that run a query to the Dozer gRPC APIs to check if some data is there.

```sh
python query.py -a <your_application_id>
```
