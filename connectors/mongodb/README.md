# Mongo DB setup

This README provides instructions for setting up a Mongo DB instance and loading data into it.

## Prerequisites

1. Log into MongoDB Atlas and create a new cluster. You can follow the instructions [here](https://docs.atlas.mongodb.com/tutorial/create-new-cluster/).
2. Load the sample data into the cluster. You can follow the instructions [here](https://www.mongodb.com/docs/atlas/sample-data/sample-analytics/).
3. Allow access to the cluster from anywhere. You can follow the instructions [here](https://docs.atlas.mongodb.com/security/ip-access-list/).
4. Setup Dozer with MongoDB enabled. You can follow the instructions 
```bash
cargo install --path dozer-cli --features cloud,mongodb --locked
```

## Steps

1. Running dozer with the following command in the terminal:
```bash
dozer run --enable-progress
```

