# Databricks Notebook
# Step 1: Read from Synapse DSP and write to raw layer

from pyspark.sql import SparkSession

jdbc_url = "jdbc:sqlserver://<your-server>.sql.azuresynapse.net:1433;database=<your-db>"
table = "dbo.sales_transactions"
properties = {
    "user": "<your-username>",
    "password": "<your-password>",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

df = spark.read.jdbc(url=jdbc_url, table=table, properties=properties)

# Write to raw catalog
df.write.format("delta").mode("overwrite").saveAsTable("raw.analytics.sales_transaction_raw")
