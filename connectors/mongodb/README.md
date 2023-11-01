# Mongo DB setup

This README provides instructions for setting up a Mongo DB instance and loading data into it.

## Prerequisites

1. Create a MongoDB account by visiting the [MongoDB website](https://www.mongodb.com/cloud/atlas) and signing up for an account.
2. Once logged in, navigate to the MongoDB web interface to create a new project.
3. Load the sample data into the cluster. You can follow the instructions [here](https://www.mongodb.com/docs/atlas/sample-data/sample-analytics/).
4. Allow access to the cluster from anywhere. You can follow the instructions [here](https://docs.atlas.mongodb.com/security/ip-access-list/).
5. Grab the connection string from the cluster. You can follow the instructions [here](https://docs.atlas.mongodb.com/tutorial/connect-to-your-cluster/).
6. Setup Dozer with MongoDB enabled. You can follow the instructions 
```bash
cargo install --path dozer-cli --features mongodb --locked
```

## Steps

1. Running dozer with the following command in the terminal:
```bash
dozer run
```

## Dozer Cloud

### To validate your config file before deploying

```bash
dozer build
```

### To deploy your config file

```bash
dozer cloud`deploy -c dozer-config.yaml 
```

### To use environment variables in the config file

```bash
dozer cloud deploy -s MONGODB_CONNECTION_STRING
```
