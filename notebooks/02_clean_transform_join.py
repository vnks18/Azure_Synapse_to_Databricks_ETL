# Enhanced version for dev branch: Data Cleaning + Feature Engineering

from pyspark.sql.functions import col, lower, when, to_date, regexp_replace, lit, months_between, current_date, round
from pyspark.sql.types import DoubleType

# Load raw transaction data
sales = spark.table("raw.analytics.sales_transaction_raw")
customers = spark.read.csv("dbfs:/mnt/data/project1/data/customer_data.csv", header=True, inferSchema=True)

# -----------------------------
# Step 1: Clean and Normalize Sales Data
# -----------------------------
sales_clean = sales.dropDuplicates(["TransactionID"])     .withColumn("Region", when(col("Region").isNull(), "Unknown").otherwise(lower(col("Region"))))     .withColumn("PaymentMode", lower(col("PaymentMode")))     .withColumn("Amount", when(col("Amount").cast(DoubleType()).isNull(), 0).otherwise(col("Amount")))     .withColumn("TransactionDate", to_date(col("TransactionDate"), "yyyy-MM-dd"))     .withColumn("DiscountPercent", when(col("DiscountApplied") == True, lit(0.10)).otherwise(lit(0.0)))     .withColumn("RegionGroup", when(col("Region").isin("north", "east"), "North-East")
                            .when(col("Region").isin("south", "west"), "South-West")
                            .otherwise("Other"))

# -----------------------------
# Step 2: Clean Customer Data
# -----------------------------
customers_clean = customers.dropDuplicates(["CustomerID"])     .withColumn("Country", when(col("Country").isNull(), "Unknown").otherwise(col("Country")))     .withColumn("SignupDate", to_date(col("SignupDate")))     .withColumn("CustomerTenureMonths", round(months_between(current_date(), col("SignupDate"))))     .withColumn("CustomerName", regexp_replace(col("CustomerName"), "[^a-zA-Z ]", ""))

# -----------------------------
# Step 3: Join + Feature Engineering
# -----------------------------
sales_joined = sales_clean.join(customers_clean, "CustomerID", "left")     .withColumn("NetAmount", round(col("Amount") * (1 - col("DiscountPercent")), 2))     .withColumn("HighValueCustomer", when(col("NetAmount") > 1500, "Yes").otherwise("No"))

# -----------------------------
# Step 4: Write to Silver Layer
# -----------------------------
sales_joined.write.format("delta").mode("overwrite").saveAsTable("main.analytics.sales_transaction_silver")

# Optional: Create a cleaned Customer Dimension table
customers_clean.select(
    "CustomerID", "CustomerName", "Country", "SignupDate", "CustomerTenureMonths", "Status", "PreferredChannel"
).write.format("delta").mode("overwrite").saveAsTable("main.analytics.customer_dim_silver")
