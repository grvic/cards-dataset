# Gold Layer - Data Dictionary

## Quick Reference Schema

### CUSTOMERS
Dimension table with customer attributes. Primary key: `customer_id`

| Column | Type | Nullable | Sample | Description |
|--------|------|----------|--------|-------------|
| customer_id | STRING | NO | CUST_000001 | Unique customer identifier |
| first_name | STRING | YES | Danielle | Customer first name |
| last_name | STRING | YES | Johnson | Customer last name |
| email | STRING | YES | john21@example.net | Email address |
| phone | STRING | YES | 001-581-896-0013x3890 | Phone number |
| date_of_birth | DATE | YES | 1960-03-10 | Birth date (age 18+) |
| address | STRING | YES | 26542 Susan Junction... | Full street address |
| city | STRING | YES | Herrerafurt | City name |
| state | STRING | YES | Colorado | State abbreviation |
| zip_code | STRING | YES | 72858 | ZIP code |
| country | STRING | YES | US | Country code |
| customer_segment | STRING | YES | Basic/Standard/Premium | Customer tier |
| account_status | STRING | YES | Active/Inactive | Account status |
| account_open_date | DATE | YES | 2023-09-05 | Account creation date |
| created_at | TIMESTAMP | YES | 2026-03-10 09:14:45 | Record load timestamp |

---

### CARDS
Dimension table with card details. Primary key: `card_id`. Foreign key: `customer_id` → CUSTOMERS

| Column | Type | Nullable | Sample | Description |
|--------|------|----------|--------|-------------|
| card_id | STRING | NO | CARD_00000350 | Unique card identifier |
| customer_id | STRING | NO | CUST_000211 | Foreign key to CUSTOMERS |
| card_brand | STRING | YES | Visa/Mastercard/Amex/Discover | Card issuer |
| card_type | STRING | YES | Credit/Debit/Business | Type of card product |
| card_number_last_4 | STRING | YES | 4527 | Last 4 digits for display |
| card_number_hash | STRING | YES | hash_... | Hashed card number |
| cardholder_name | STRING | YES | Danielle Johnson | Name on card |
| expiry_month | INTEGER | YES | 7 | Expiration month (1-12) |
| expiry_year | INTEGER | YES | 2028 | Expiration year |
| is_default | BOOLEAN | YES | true/false | Primary card flag |
| card_status | STRING | YES | Active/Blocked/Expired | Card status |
| issued_date | DATE | YES | 2023-09-05 | Card issuance date |
| created_at | TIMESTAMP | YES | 2026-03-10 09:14:45 | Record load timestamp |

---

### MERCHANTS
Dimension table with merchant information. Primary key: `merchant_id`

| Column | Type | Nullable | Sample | Description |
|--------|------|----------|--------|-------------|
| merchant_id | STRING | NO | MERCH_000027 | Unique merchant identifier |
| merchant_name | STRING | YES | Ashley, Ross and Cruz | Merchant business name |
| merchant_category | STRING | YES | Automotive/Grocery/... | Business category |
| country | STRING | YES | US | Country code |
| city | STRING | YES | Denver | City location |
| state | STRING | YES | Colorado | State location |
| merchant_id_industry | STRING | YES | MCC_6177 | Merchant Category Code |
| created_at | TIMESTAMP | YES | 2026-03-10 09:14:45 | Record load timestamp |

**Merchant Categories (15 types):**
Grocery, Gas Station, Restaurant, Hotel, Airlines, Retail, Entertainment, Utilities, Healthcare, Online Shopping, Subscription, Automotive, Pharmacy, Coffee Shop, Gym

---

### TRANSACTIONS
Fact table with all transaction records. Primary key: `transaction_id`. Foreign keys: `card_id` → CARDS, `customer_id` → CUSTOMERS, `merchant_id` → MERCHANTS

| Column | Type | Nullable | Sample | Description |
|--------|------|----------|--------|-------------|
| transaction_id | STRING | NO | TXN_000000001 | Unique transaction identifier |
| card_id | STRING | NO | CARD_00000350 | Foreign key to CARDS |
| customer_id | STRING | NO | CUST_000211 | Foreign key to CUSTOMERS |
| merchant_id | STRING | NO | MERCH_000027 | Foreign key to MERCHANTS |
| merchant_name | STRING | YES | Ashley, Ross and Cruz | Merchant name (denormalized) |
| merchant_category | STRING | YES | Automotive | Merchant category (denormalized) |
| amount | DECIMAL(10,2) | YES | 39.61 | Transaction amount in USD |
| currency | STRING | YES | USD | Currency code |
| transaction_type | STRING | YES | Purchase/Withdrawal/Transfer | Type of transaction |
| transaction_status | STRING | YES | Completed/Pending/Declined | Status of transaction |
| transaction_date | DATE | YES | 2025-05-11 | Date of transaction |
| transaction_time | TIME | YES | 09:14:46 | Time of transaction |
| transaction_timestamp | TIMESTAMP | YES | 2025-05-11 09:14:46 | Full datetime |
| mcc_code | STRING | YES | MCC_6177 | Merchant Category Code |
| is_fraud | BOOLEAN | YES | false | Fraud flag (TRUE = suspicious) |
| created_at | TIMESTAMP | YES | 2026-03-10 09:14:46 | Record load timestamp |

**Transaction Status Distribution:**
- Completed: ~95% (successful transactions)
- Declined: ~3% (failed authorizations)
- Pending: ~2% (unresolved)

---

### CUSTOMER_SPENDING_SUMMARY
Fact table - aggregated customer metrics. One row per customer. Primary key: `customer_id`

| Column | Type | Nullable | Sample | Description |
|--------|------|----------|--------|-------------|
| customer_id | STRING | NO | CUST_000001 | Unique customer identifier |
| total_transactions | INTEGER | YES | 12 | Count of transactions |
| total_spending | DECIMAL(12,2) | YES | 2145.67 | Sum of transaction amounts |
| average_transaction_amount | DECIMAL(10,2) | YES | 178.81 | Mean transaction value |
| max_transaction_amount | DECIMAL(10,2) | YES | 892.34 | Largest transaction |
| active_cards | INTEGER | YES | 2 | Count of active cards |
| total_cards | INTEGER | YES | 3 | Total cards owned |
| fraud_transactions | INTEGER | YES | 2 | Count of fraudulent txns |
| fraud_rate | DECIMAL(5,4) | YES | 0.1667 | Fraud rate (0-1 scale) |
| last_transaction_date | DATE | YES | 2026-03-01 | Most recent transaction |
| days_since_last_transaction | INTEGER | YES | 9 | Days since last activity |
| created_at | TIMESTAMP | YES | 2026-03-10 09:14:45 | Record load timestamp |

---

### MERCHANT_PERFORMANCE_SUMMARY
Fact table - aggregated merchant metrics. One row per merchant. Primary key: `merchant_id`

| Column | Type | Nullable | Sample | Description |
|--------|------|----------|--------|-------------|
| merchant_id | STRING | NO | MERCH_000027 | Unique merchant identifier |
| merchant_name | STRING | YES | Ashley, Ross and Cruz | Merchant name |
| merchant_category | STRING | YES | Automotive | Business category |
| total_transactions | INTEGER | YES | 18 | Total transactions processed |
| total_volume | DECIMAL(12,2) | YES | 1234.56 | Total transaction amount |
| average_transaction_amount | DECIMAL(10,2) | YES | 68.59 | Mean transaction value |
| total_customers | INTEGER | YES | 15 | Unique customers |
| fraud_transactions | INTEGER | YES | 3 | Fraudulent transactions |
| fraud_rate | DECIMAL(5,4) | YES | 0.1667 | Fraud rate (0-1 scale) |
| created_at | TIMESTAMP | YES | 2026-03-10 09:14:46 | Record load timestamp |

---

### DAILY_TRANSACTIONS_SUMMARY
Fact table - daily aggregated metrics. One row per day. Primary key: `date`

| Column | Type | Nullable | Sample | Description |
|--------|------|----------|--------|-------------|
| date | DATE | NO | 2025-03-15 | Calendar date |
| total_transactions | INTEGER | YES | 45 | Transactions that day |
| total_volume | DECIMAL(12,2) | YES | 7234.89 | Daily transaction sum |
| average_transaction_amount | DECIMAL(10,2) | YES | 160.78 | Mean transaction value |
| unique_customers | INTEGER | YES | 35 | Unique customers |
| unique_merchants | INTEGER | YES | 28 | Unique merchants |
| fraud_transactions | INTEGER | YES | 7 | Fraudulent transactions |
| fraud_rate | DECIMAL(5,4) | YES | 0.1556 | Daily fraud rate |

---

## Data Type Mappings

For different databases/platforms:

### PostgreSQL
```sql
-- STRING → VARCHAR(255)
-- INTEGER → INT
-- DECIMAL → NUMERIC(10,2)
-- BOOLEAN → BOOLEAN
-- DATE → DATE
-- TIMESTAMP → TIMESTAMP
```

### Snowflake
```sql
-- STRING → VARCHAR(255)
-- INTEGER → INTEGER
-- DECIMAL → DECIMAL(10,2)
-- BOOLEAN → BOOLEAN
-- DATE → DATE
-- TIMESTAMP → TIMESTAMP_NTZ
```

### BigQuery
```sql
-- STRING → STRING
-- INTEGER → INT64
-- DECIMAL → NUMERIC
-- BOOLEAN → BOOL
-- DATE → DATE
-- TIMESTAMP → TIMESTAMP
```

### Redshift
```sql
-- STRING → VARCHAR(255)
-- INTEGER → INTEGER
-- DECIMAL → NUMERIC(10,2)
-- BOOLEAN → BOOLEAN
-- DATE → DATE
-- TIMESTAMP → TIMESTAMP
```

---

## SQL Join Patterns

### Get customer spending with details
```sql
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    cs.total_transactions,
    cs.total_spending,
    cs.fraud_transactions
FROM customers c
LEFT JOIN customer_spending_summary cs ON c.customer_id = cs.customer_id
ORDER BY cs.total_spending DESC;
```

### Get merchant performance with transaction details
```sql
SELECT 
    m.merchant_id,
    m.merchant_name,
    m.merchant_category,
    mp.total_transactions,
    mp.total_volume,
    mp.fraud_rate
FROM merchants m
LEFT JOIN merchant_performance_summary mp ON m.merchant_id = mp.merchant_id
ORDER BY mp.total_volume DESC;
```

### Get customer transactions with all details
```sql
SELECT 
    t.transaction_id,
    c.customer_id,
    c.first_name,
    c.last_name,
    ca.card_id,
    m.merchant_name,
    m.merchant_category,
    t.amount,
    t.transaction_date,
    t.is_fraud
FROM transactions t
JOIN customers c ON t.customer_id = c.customer_id
JOIN cards ca ON t.card_id = ca.card_id
JOIN merchants m ON t.merchant_id = m.merchant_id
ORDER BY t.transaction_timestamp DESC;
```

---

## Statistics by Column

### TRANSACTIONS
| Field | Min | Max | Mean | Median |
|-------|-----|-----|------|--------|
| amount | $5.12 | $1,499.87 | $177.47 | $142.33 |
| fraud_rate | 0% | 100% | 16.58% | - |

### CUSTOMERS
| Field | Count | Unique | %Null |
|-------|-------|--------|-------|
| customer_segment | 500 | 3 | 0% |
| account_status | 500 | 2 | 0% |
| Active accounts | 363 | - | - |

### CARDS  
| Field | Count | Unique | %Null |
|-------|-------|--------|-------|
| card_status | 820 | 3 | 0% |
| card_brand | 820 | 4 | 0% |
| card_type | 820 | 3 | 0% |

---

## Import Examples

### Load into SQL Server
```sql
BULK INSERT customers
FROM 'D:\data\customers.csv'
WITH (
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    FIRSTROW = 2
);
```

### Load into pandas (Python)
```python
import pandas as pd

customers = pd.read_csv('customers.csv')
cards = pd.read_csv('cards.csv')
merchants = pd.read_csv('merchants.csv')
transactions = pd.read_csv('transactions.csv')
```

### Load into Tableau
1. Open Tableau
2. Connect → Text File → Select CSV
3. Browse to gold/ folder and select any CSV
4. Adjust field types as needed
5. Use Customer_spending_summary for quick dashboards

---

**Last Updated**: March 10, 2026  
**Data Quality**: ✓ Validated  
**Ready for Production**: Yes
