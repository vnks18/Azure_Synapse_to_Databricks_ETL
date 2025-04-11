# Project: Azure Synapse DSP to Databricks Unity Catalog

## 📌 Objective

This project demonstrates a practical migration workflow for moving data from **Azure Synapse Dedicated SQL Pool (DSP)** to **Databricks Unity Catalog**, using Delta Lake's **raw** and **silver** layers. The pipeline includes reading from Synapse, data cleansing, enrichment, and writing to Delta format tables for analytics.

---

## 📂 Project Structure

```
AzureSynapse_To_Databricks_Migration/
│
├── data/                           # Dummy 100MB+ realistic data
│   ├── sales_transactions.csv
│   └── customer_data.csv
│
├── notebooks/                      # PySpark scripts
│   ├── 01_dsp_read_to_raw.py
│   ├── 02_clean_transform_join.py
│   └── utils.py
│
├── catalog/                        # SQL schema definition for DSP and for catalog in databricks
│   └── schema_definition.sql
│
├── architecture.png                # Visual pipeline diagram
├── README.md                       # This file
└── requirements.txt
```

---

## 🧠 Why Migrate to Databricks?

| Feature                  | Synapse DSP       | Databricks Lakehouse    |
|--------------------------|-------------------|--------------------------|
| Compute Flexibility      | Fixed DWU (pre-allocated)         | Auto-scale clusters      |
| Data Format Support      | Tabular only      | Delta, Parquet, CSV, JSON |
| Streaming Support        | Limited           | Built-in Streaming       |
| Cost Efficiency          | High on idle DSP  | Pay-per-use              |
| ML & Data Science        | Separate services | Native to workspace (MLlib, notebooks)     |
| Orchestration            | Basic pipelines   | Complex orchestration + APIs    |
| Catalog Management       | Limited             | Unity Catalog (RBAC, lineage)    |

---

## 🔧 Processing Steps

### Step 1: Read from Synapse DSP → Raw Layer
- Ingest data using JDBC from DSP
- Store in Unity Catalog: `raw.analytics.sales_transaction_raw`

### Step 2: Clean & Transform → Silver Layer
- Normalize strings, handle nulls, correct types
- Join with `customer_data.csv`
- Derive `NetAmount` after discount
- Write to: `main.analytics.sales_transaction_silver`

---

## 🧪 Data Preview / Schema

**Sales Transactions (100k rows)**  
Columns: `TransactionID`, `CustomerID`, `TransactionDate`, `Region`, `ProductCategory`, `Amount`, `PaymentMode`, `DeliveryStatus`, `Rating`, `CustomerFeedback`, ...

**Customer Data (5k rows)**  
Columns: `CustomerID`, `CustomerName`, `Email`, `Country`, `SignupDate`, `Status`, `PreferredChannel`, ...

---

## 🖼️ Architecture

![Architecture](architecture.png)

---

## 🔌 Connections & Config

Update `jdbc_url`, `user`, and `password` in:
```python
notebooks/01_dsp_read_to_raw.py
notebooks/utils.py
```

---

## 🚀 How to Use

1. Upload `sales_transactions.csv` and `customer_data.csv` to Databricks DBFS or external storage.
2. Update JDBC configs in `01_dsp_read_to_raw.py` and `utils.py`.
3. Run notebooks in sequence.
4. For improved logic, use `02_clean_transform_join.py`.

---

## ✅ Output Tables

| Layer   | Catalog  | Schema    | Table                            |
|---------|----------|-----------|----------------------------------|
| Raw     | raw      | analytics | sales_transaction_raw           |
| Silver  | main     | analytics | sales_transaction_silver        |

---

## 📈 Future Steps

- Add gold layer aggregations
- Integrate with Power BI via Databricks SQL
- Monitor schema changes and automate catalog registration

---
