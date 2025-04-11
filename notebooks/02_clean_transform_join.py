# Databricks Notebook
# Step 2: Clean, transform, and join datasets → Silver Layer

from pyspark.sql.functions import col, lower, when, to_date, isnan, isnull, regexp_replace

# Load raw data
sales = spark.table("raw.analytics.sales_transaction_raw")
customers = spark.read.csv("dbfs:/mnt/data/project1/data/customer_data.csv", header=True, inferSchema=True)

# Basic clean-up
sales_clean = sales.dropDuplicates(["TransactionID"]).withColumn("Region", when(col("Region").isNull(), "Unknown").otherwise(col("Region"))).withColumn("Amount", when(col("Amount") < 0, 0).otherwise(col("Amount"))).withColumn("PaymentMode", lower(col("PaymentMode"))).withColumn("TransactionDate", to_date(col("TransactionDate")))

# Customer cleanup
customers_clean = customers.withColumn("CustomerName", regexp_replace(col("CustomerName"), "[^a-zA-Z ]", "")).withColumn("Country", when(col("Country").isNull(), "Unknown").otherwise(col("Country"))).dropDuplicates(["CustomerID"])

# Join
sales_joined = sales_clean.join(customers_clean, "CustomerID", "left").withColumn("NetAmount", col("Amount") * when(col("DiscountApplied") == True, 0.9).otherwise(1.0))

# Write to silver layer
sales_joined.write.format("delta").mode("overwrite").saveAsTable("main.analytics.sales_transaction_silver")
