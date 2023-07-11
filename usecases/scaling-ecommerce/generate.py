import dbldatagen as dg

import pyspark
from delta import *
from pyspark.sql.types import IntegerType

builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.driver.memory", "2g")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Create the tables using Delta format if they don't exist
spark.sql("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INT,
        name STRING,
        email STRING,
        address STRING,
        created_at TIMESTAMP
    )
    USING Delta
""")

spark.sql("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT,
        customer_id INT,
        order_date TIMESTAMP,
        total_amount DOUBLE
    )
    USING Delta
""")

spark.sql("""
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INT,
        order_id INT,
        product_id INT,
        quantity INT,
        price DOUBLE,
        
        field_01 STRING,
        field_02 STRING,
        field_03 STRING,
        field_04 STRING,
        field_05 STRING,
        field_06 STRING,
        field_07 STRING,
        field_08 STRING,
        field_09 STRING,
        field_10 STRING,
        field_11 STRING,
        field_12 STRING,
        field_13 STRING,
        field_14 STRING,
        field_15 STRING,
        field_16 STRING
        
    )
    USING Delta
""")

spark.sql("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INT,
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
        dg.DataGenerator(spark, rows=10_000_000, partitions=8)
        .withSchema(customers_schema)
        .withColumnSpec("customer_id", minValue=1, maxValue=10_000_000, step=1)
        .withColumnSpec("name", template=r"\w{5,10} \w{5,10}")
        .withColumnSpec("email", template=r"\w{5,10}@\w{5,10}.com")
        .withColumnSpec("address", template=r"\w{5,10} Street, City")
        .withColumnSpec("created_at", minValue="2022-01-01", maxValue="2022-12-31")
      )

orders_dataspec = (
        dg.DataGenerator(spark, rows=10_000_000, partitions=8)
        .withSchema(orders_schema)
        .withColumnSpec("order_id", minValue=10_000_001, maxValue=20_000_000, step=1)
        .withColumnSpec("customer_id", minValue=1, maxValue=10_000_000, step=1)
        .withColumnSpec("order_date", minValue="2022-01-01", maxValue="2022-12-31")
        .withColumnSpec("total_amount", minValue=10, maxValue=1000)
      )

order_items_dataspec = (
        dg.DataGenerator(spark, rows=100_000_000, partitions=8)
        .withSchema(order_items_schema)
        .withColumnSpec("order_item_id", minValue=100_000_001, maxValue=200_000_000, step=1)
        .withColumnSpec("order_id", minValue=10_000_001, maxValue=20_000_000, step=1)
        .withColumnSpec("product_id", minValue=20_000_001, maxValue=30_000_000, step=1)
        .withColumnSpec("quantity", minValue=1, maxValue=10)
        .withColumnSpec("price", minValue=10.0, maxValue=100.0)
        .withColumnSpec("field_01", template=r"\w{32}")
        .withColumnSpec("field_02", template=r"\w{32}")
        .withColumnSpec("field_03", template=r"\w{32}")
        .withColumnSpec("field_04", template=r"\w{32}")
        .withColumnSpec("field_05", template=r"\w{32}")
        .withColumnSpec("field_06", template=r"\w{32}")
        .withColumnSpec("field_07", template=r"\w{32}")
        .withColumnSpec("field_08", template=r"\w{32}")
        .withColumnSpec("field_09", template=r"\w{32}")
        .withColumnSpec("field_10", template=r"\w{32}")
        .withColumnSpec("field_11", template=r"\w{32}")
        .withColumnSpec("field_12", template=r"\w{32}")
        .withColumnSpec("field_13", template=r"\w{32}")
        .withColumnSpec("field_14", template=r"\w{32}")
        .withColumnSpec("field_15", template=r"\w{32}")
        .withColumnSpec("field_16", template=r"\w{32}")
    )

products_dataspec = (
        dg.DataGenerator(spark, rows=10_000_000, partitions=8)
        .withSchema(products_schema)
        .withColumnSpec("product_id", minValue=20_000_001, maxValue=30_000_000, step=1)
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
