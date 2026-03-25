# Gold Layer - Synthetic Card Data Analytics Dataset

## Overview
This is a complete, production-ready synthetic card dataset organized in the gold layer, optimized for analytics and business intelligence. The dataset includes 7,585 total records across 7 interconnected tables.

## Dataset Contents

### 1. **customers.csv** (500 rows)
Core customer dimension table with complete customer information.
- **customer_id**: Unique customer identifier (CUST_XXXXXX)
- **first_name, last_name**: Customer name
- **email, phone**: Contact information
- **date_of_birth**: Age information
- **address, city, state, zip_code, country**: Demographic data
- **customer_segment**: Premium, Standard, or Basic
- **account_status**: Active or Inactive
- **account_open_date**: Account creation date
- **created_at**: Record creation timestamp

### 2. **cards.csv** (820 rows)
Credit/debit card dimension table. Each customer has 1-3 cards.
- **card_id**: Unique card identifier (CARD_XXXXXXXX)
- **customer_id**: Reference to customer
- **card_brand**: Visa, Mastercard, American Express, Discover
- **card_type**: Credit, Debit, or Business
- **card_number_last_4**: Last 4 digits for display
- **card_number_hash**: Hashed card number for security
- **cardholder_name**: Name on card
- **expiry_month, expiry_year**: Card expiration
- **is_default**: Whether this is the customer's default card
- **card_status**: Active, Blocked, or Expired

### 3. **merchants.csv** (200 rows)
Merchant dimension table with merchant details.
- **merchant_id**: Unique merchant identifier (MERCH_XXXXXX)
- **merchant_name**: Name of the business
- **merchant_category**: 15 categories (Grocery, Gas, Restaurant, Hotel, etc.)
- **country, city, state**: Merchant location
- **merchant_id_industry**: MCC (Merchant Category Code)
- **created_at**: Record creation timestamp

### 4. **transactions.csv** (5,000 rows)
Fact table of all transactions. This is the main transactional dataset.
- **transaction_id**: Unique transaction identifier (TXN_XXXXXXXXX)
- **card_id**: Reference to card used
- **customer_id**: Reference to customer
- **merchant_id**: Reference to merchant
- **merchant_name, merchant_category**: Merchant details
- **amount**: Transaction amount in USD
- **currency**: Currency code (USD)
- **transaction_type**: Purchase, Withdrawal, or Transfer
- **transaction_status**: Completed, Pending, or Declined
- **transaction_date, transaction_time**: When transaction occurred
- **transaction_timestamp**: Full datetime
- **mcc_code**: Merchant category code
- **is_fraud**: Boolean flag for fraud detection
- **created_at**: Record creation timestamp

### 5. **customer_spending_summary.csv** (500 rows)
Customer-level aggregated analytics table. One row per customer.
- **customer_id**: Reference to customer
- **total_transactions**: Number of transactions
- **total_spending**: Sum of all transaction amounts
- **average_transaction_amount**: Mean transaction value
- **max_transaction_amount**: Largest single transaction
- **active_cards**: Count of active cards
- **total_cards**: Total cards owned
- **fraud_transactions**: Count of flagged fraudulent transactions
- **fraud_rate**: Fraud transaction percentage
- **last_transaction_date**: Most recent transaction
- **days_since_last_transaction**: Days since customer's last activity
- **created_at**: Record creation timestamp

### 6. **merchant_performance_summary.csv** (200 rows)
Merchant-level aggregated analytics table. One row per merchant.
- **merchant_id**: Reference to merchant
- **merchant_name**: Merchant business name
- **merchant_category**: Type of business
- **total_transactions**: Number of transactions processed
- **total_volume**: Sum of transaction amounts
- **average_transaction_amount**: Mean transaction value
- **total_customers**: Count of unique customers
- **fraud_transactions**: Count of flagged fraudulent transactions
- **fraud_rate**: Fraud transaction percentage
- **created_at**: Record creation timestamp

### 7. **daily_transactions_summary.csv** (365 rows)
Time series analytics table. One row per day with transaction activity.
- **date**: Calendar date
- **total_transactions**: Number of transactions that day
- **total_volume**: Daily transaction amount
- **average_transaction_amount**: Mean transaction value
- **unique_customers**: Count of unique customers transacting
- **unique_merchants**: Count of unique merchants
- **fraud_transactions**: Count of fraudulent transactions
- **fraud_rate**: Daily fraud percentage

## Key Statistics

| Metric | Value |
|--------|-------|
| Total Records | 7,585 |
| Date Range | Mar 10, 2025 - Mar 09, 2026 |
| Total Transaction Volume | $887,369.10 |
| Overall Fraud Rate | 16.58% |
| Active Customer Accounts | 363 |
| Cards per Customer (avg) | 1.64 |
| Merchants Covered | 200 |

## Data Quality

✓ **No missing values** - All critical fields are populated  
✓ **Realistic distributions** - Transaction amounts vary by merchant type  
✓ **Proper relationships** - Foreign key relationships intact  
✓ **Date consistency** - All dates within valid range  
✓ **Anonymized** - Customer data is synthetic and safe for testing  

## Use Cases

This dataset is ready for:
- **Dashboard Development**: Build BI dashboards with ready-to-use aggregated tables
- **Fraud Analysis**: Study transaction patterns and fraud indicators
- **Customer Analytics**: Analyze spending behavior and segments
- **Merchant Performance**: Track top merchants and categories
- **Time Series Analysis**: Use daily summaries for trend analysis
- **Testing & Development**: Safe synthetic data for development/testing
- **Machine Learning**: Train fraud detection or customer models

## Analytics Insights

### Customer Segmentation
```
Premium:  ~33% of customers (highest spending)
Standard: ~33% of customers (moderate spending)
Basic:    ~33% of customers (lower spending)
```

### Merchant Categories
- Top categories: Grocery, Restaurant, Retail, Gas Station
- Each merchant has realistic transaction patterns
- Fraud rates vary by category

### Transaction Patterns
- Average transaction: ~$177
- Transaction amounts vary realistically by merchant type
- ~16.6% fraud rate provides realistic detection scenarios

## File Size Reference

| File | Size |
|------|------|
| customers.csv | ~80 KB |
| cards.csv | ~95 KB |
| merchants.csv | ~25 KB |
| transactions.csv | ~650 KB |
| customer_spending_summary.csv | ~70 KB |
| merchant_performance_summary.csv | ~30 KB |
| daily_transactions_summary.csv | ~45 KB |
| **Total** | **~995 KB** |

## Related Tables (Foreign Keys)

```
customers
    ├── One-to-Many → cards
    └── One-to-Many → transactions
    
merchants
    └── One-to-Many → transactions

cards
    └── One-to-Many → transactions

transactions
    ├── Many-to-One → customers
    ├── Many-to-One → cards
    └── Many-to-One → merchants

customer_spending_summary
    └── One-to-One → customers

merchant_performance_summary
    └── One-to-One → merchants

daily_transactions_summary
    └── Many-to-One → transactions
```

## Getting Started

1. **Load into Your Analytics Tool**: Import CSVs into your BI tool (Tableau, Power BI, Looker, etc.)
2. **Create Primary Keys**: transactions.csv is fact table
3. **Use Summary Tables**: For reports, use pre-aggregated customer/merchant tables
4. **Time Series Analysis**: Use daily_transactions_summary.csv for trend analysis
5. **Fraud Detection**: Explore is_fraud flag in transactions for ML modeling

## Column Data Types (for SQL Import)

```sql
-- For reference when importing to database
customer_id: VARCHAR(10)
card_id: VARCHAR(12)
merchant_id: VARCHAR(10)
transaction_id: VARCHAR(12)
amount: DECIMAL(10,2)
transaction_date: DATE
transaction_timestamp: DATETIME
is_fraud: BOOLEAN
```

## Notes

- All customer and card data is **100% synthetic** and generated by the Faker library
- Fraud flags are randomly assigned (~16.6% rate) for testing purposes
- Data spans exactly 365 days for consistent daily summaries
- Card numbers are properly formatted but hashed for security
- All amounts are in USD currency

---

**Generated**: March 10, 2026  
**Total Dataset**: $887,369.10 in transaction volume  
**Status**: ✓ Production Ready for Analytics
