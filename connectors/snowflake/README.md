## Snowflake example

This example shows how to use sample supabase postgres table as data source in Dozer

First, expose environment variables which maps your snowflake credentials into
```bash
export SN_SERVER=
export SN_USER=
export SN_PASSWORD=
export SN_DATABASE=
export SN_WAREHOUSE=
export SN_ROLE=
```

Running Dozer
```
docker-compose up
```

That's all to it. This process will run `dozer app` and `dozer api` server separately and you will have APIs instantly available over REST and gRPC.
