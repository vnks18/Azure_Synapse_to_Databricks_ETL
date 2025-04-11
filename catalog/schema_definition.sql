-- Catalog schema for raw and silver tables in Unity Catalog

-- RAW TABLE
CREATE TABLE raw.analytics.sales_transaction_raw (
    TransactionID INT,
    CustomerID INT,
    TransactionDate DATE,
    Region STRING,
    ProductCategory STRING,
    Amount DOUBLE,
    PaymentMode STRING,
    DiscountApplied BOOLEAN,
    DeliveryStatus STRING,
    Rating INT,
    CustomerFeedback STRING
)
USING DELTA;

-- SILVER TABLE
CREATE TABLE main.analytics.sales_transaction_silver (
    TransactionID INT,
    CustomerID INT,
    TransactionDate DATE,
    Region STRING,
    ProductCategory STRING,
    Amount DOUBLE,
    PaymentMode STRING,
    DiscountApplied BOOLEAN,
    DeliveryStatus STRING,
    Rating INT,
    CustomerFeedback STRING,
    CustomerName STRING,
    Country STRING,
    SignupDate DATE,
    Status STRING,
    Age INT,
    PreferredChannel STRING,
    IsSubscribed BOOLEAN,
    NetAmount DOUBLE
)
USING DELTA;

-- OPTIONAL CUSTOMER DIM TABLE
CREATE TABLE main.analytics.customer_dim_silver (
    CustomerID INT,
    CustomerName STRING,
    Country STRING,
    SignupDate DATE,
    Status STRING,
    Age INT,
    PreferredChannel STRING,
    IsSubscribed BOOLEAN
)
USING DELTA;
