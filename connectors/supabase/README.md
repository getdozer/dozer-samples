## Supabase Postgres example

This example shows how to use sample supabase postgres table as data source in Dozer

```bash
export PG_USER=postgres
export PG_PASSWORD=postgres-dozer-123
export PG_HOST=db.wlpfvdagkydbanuiqvjy.supabase.co
export PG_DB=postgres
```

Running Dozer
```
docker-compose up
```

That's all to it. This process will run `dozer app` and `dozer api` server separately and you will have APIs instantly available over REST and gRPC.
