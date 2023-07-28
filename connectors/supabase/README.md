## Supabase Postgres example

This example shows how to use sample supabase postgres table as data source in Dozer

```bash
export PG_USER=${PG_USER}
export PG_PASSWORD=${PG_PASSWORD}
export PG_HOST=${PG_HOST}
export PG_DB=${PG_DB}
```

Running Dozer
```
docker-compose up
```

That's all to it. This process will run `dozer app` and `dozer api` server separately and you will have APIs instantly available over REST and gRPC.
