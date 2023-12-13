# Temporal + Dozer

The basic premise of this demo is an eCommerce workflow:

1. User places order
2. Record order in PG database
3. Check that there is enough stock in the warehouse (PG + CSV -> Dozer)
4. Fulfil order (write to PG database)

This is supported by a workflow to refill the warehouse's stock which does:

1. Check how much to order (PG + CSV -> Dozer)
2. Record the stock refill (write CSV)

On top of all this is a dozer dashboard API, which combines a MongoDB listings
collection with the output of the warehouse stock dozer instance

Detailed article present on [Dozer blog](https://getdozer.io/blog/temporal-dozer/)

# Folder structure

- `data`: listings dataset. Import into mongodb using `zcat data/listings/metadata/listings_0.json.gz | mongoimport --db products --collection listings`. You can import more than just the first file, but you might run out of memory ([#2214](https://github.com/getdozer/dozer/pull/2214) helps with that)
- `init/orders.sql`: postgres schema
- `workflows/`: temporal workflows. Currently only the first step of the order placement workflow is implemented.
- `worker.py`: temporal worker. Needs to be run for the workflow to make progress.
- `warehouse_logs/logs/`: warehouse order log CSVs. Schema: `product_id(string),amount(int)`
- `dozer/`: the two dozer applications. The `dashboard` app depends on the `fulfillment` app
