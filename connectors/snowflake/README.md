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

## Dozer Cloud

### Validate the Config file before deploying

```bash
dozer build
```

### To deploy

```bash
dozer cloud deploy
```

### To use environment variables in the config file

```bash
dozer cloud deploy -s SN_SERVER=$SN_SERVER -s SN_USER=$SN_USER -s SN_PASSWORD=$SN_PASSWORD -s SN_DATABASE=$SN_DATABASE -s SN_WAREHOUSE=$SN_WAREHOUSE -s SN_ROLE=$SN_ROLE
```

Running Dozer
```
docker-compose up
```

That's all to it. This process will run `dozer app` and `dozer api` server separately and you will have APIs instantly available over REST and gRPC.

