import dbldatagen as dg

import pyspark
from delta import *

builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Create the tables using Delta format if they don't exist
spark.sql("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id STRING,
        name STRING,
        email STRING,
        address STRING,
        created_at TIMESTAMP
    )
    USING Delta
""")

spark.sql("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id STRING,
        customer_id STRING,
        order_date TIMESTAMP,
        total_amount DOUBLE
    )
    USING Delta
""")

spark.sql("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id STRING,
        order_id STRING,
        product_id STRING,
        quantity INT,
        price DOUBLE
    )
    USING Delta
""")

spark.sql("""
    CREATE TABLE IF NOT EXISTS products (
        product_id STRING,
        name STRING,
        category STRING,
        price DOUBLE,
        created_at TIMESTAMP
    )
    USING Delta
""")

# Get the table schemas
customers_schema = spark.table("customers").schema
orders_schema = spark.table("orders").schema
order_items_schema = spark.table("order_items").schema
products_schema = spark.table("products").schema



# Define column specifications for data generation
customers_dataspec = (
        dg.DataGenerator(spark, rows=10000000, partitions=8)
        .withSchema(customers_schema)
        .withColumnSpec("customer_id", template=r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}")
        .withColumnSpec("name", template=r"\w{5,10} \w{5,10}")
        .withColumnSpec("email", template=r"\w{5,10}@\w{5,10}.com")
        .withColumnSpec("address", template=r"\w{5,10} Street, City")
        .withColumnSpec("created_at", minValue="2022-01-01", maxValue="2022-12-31")
      )

orders_dataspec = (
        dg.DataGenerator(spark, rows=10000000, partitions=8)
        .withSchema(orders_schema)
         .withColumnSpec("order_id", template=r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}")
        .withColumnSpec("customer_id", template=r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}")
        .withColumnSpec("order_date", minValue="2022-01-01", maxValue="2022-12-31")
        .withColumnSpec("total_amount", minValue=10, maxValue=1000)
      )

order_items_dataspec = (
        dg.DataGenerator(spark, rows=10000000, partitions=8)
        .withSchema(order_items_schema)
        .withColumnSpec("order_item_id", template=r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}")
        .withColumnSpec("order_id", template=r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}")
        .withColumnSpec("product_id", template=r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}")
        .withColumnSpec("quantity", minValue=1, maxValue=10)
        .withColumnSpec("price", minValue=10.0, maxValue=100.0)
    )

products_dataspec = (
        dg.DataGenerator(spark, rows=10000000, partitions=8)
        .withSchema(products_schema)
        .withColumnSpec("product_id", template=r"\w{8}-\w{4}-\w{4}-\w{4}-\w{12}")
        .withColumnSpec("name", template=r"Product \w{5,10}")
        .withColumnSpec("category", template=r"\w{5,10}")
        .withColumnSpec("price", minValue=10.0, maxValue=100.0)
        .withColumnSpec("created_at", minValue="2022-01-01", maxValue="2022-12-31")
      )

# Generate the data
customers_data = customers_dataspec.build()
orders_data = orders_dataspec.build()
order_items_data = order_items_dataspec.build()
products_data = products_dataspec.build()

# Save the generated data as Delta tables
customers_data.write.format("delta").mode("overwrite").saveAsTable("customers")
orders_data.write.format("delta").mode("overwrite").saveAsTable("orders")
order_items_data.write.format("delta").mode("overwrite").saveAsTable("order_items")
products_data.write.format("delta").mode("overwrite").saveAsTable("products")
