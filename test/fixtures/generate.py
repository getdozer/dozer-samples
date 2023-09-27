# Run this in the ingest sample to generate a small.parquet file
import polars as pl

df = pl.read_parquet('data/trips/fhvhv_tripdata_2022-01.parquet')
small = df.head(100)
small.write_parquet('./small.parquet')