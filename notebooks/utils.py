# Helper configs
def get_synapse_jdbc():
    return {
        "url": "jdbc:sqlserver://<your-server>.sql.azuresynapse.net:1433;database=<your-db>",
        "user": "<your-username>",
        "password": "<your-password>",
        "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    }
