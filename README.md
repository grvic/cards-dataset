# Cards Dataset - Synthetic Payment Card Data Generator

A complete, production-ready synthetic payment card dataset generator for analytics, testing, and business intelligence workflows. This project generates realistic, interconnected datasets including customers, payment cards, merchants, transactions, and aggregated analytics.

## 📋 Overview

The **Cards Dataset** project generates a comprehensive synthetic dataset simulating real-world payment card transactions. It's designed for:

- **Data Analytics**: Practice analytics on realistic transaction data
- **Testing & QA**: Validate analytics pipelines and business intelligence tools
- **Machine Learning**: Train fraud detection and customer segmentation models
- **Demos & Education**: Provide sample data for presentations and training

## 📊 Dataset Contents

The project generates **7,585 total records** across 7 interconnected CSV tables:

| Table | Rows | Description |
|-------|------|-------------|
| **customers.csv** | 500 | Customer dimension with demographics, segments, account info |
| **cards.csv** | 820 | Payment cards with brands, types, and status |
| **merchants.csv** | 200 | Merchant dimension with categories and locations |
| **transactions.csv** | 5,000 | Fact table with all transaction records |
| **customer_spending_summary.csv** | 500 | Customer-level aggregated metrics |
| **merchant_performance_summary.csv** | 200 | Merchant-level analytics |
| **daily_transactions_summary.csv** | 365 | Time-series daily transaction summaries |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Required packages: `pandas`, `numpy`, `faker`

### Installation

1. **Clone or download the repository**

2. **Install dependencies**
   ```bash
   pip install pandas numpy faker
   ```

3. **Generate the dataset**
   ```bash
   python generate_card_data.py
   ```

   This creates a `gold/` directory with all CSV files.

## 📁 Project Structure

```
cards-dataset/
├── README.md                          # This file
├── generate_card_data.py              # Python script to generate synthetic data
└── gold/                              # Generated dataset (gold layer)
    ├── customers.csv                  # Customer dimension table
    ├── cards.csv                      # Payment cards dimension table
    ├── merchants.csv                  # Merchant dimension table
    ├── transactions.csv               # Transaction fact table
    ├── customer_spending_summary.csv  # Customer analytics
    ├── merchant_performance_summary.csv # Merchant analytics
    ├── daily_transactions_summary.csv # Time-series analytics
    ├── README.md                      # Detailed dataset documentation
    └── DATA_DICTIONARY.md             # Complete schema reference
```

## 📋 Data Dictionary

For detailed information about each table and column, see:
- **[gold/README.md](gold/README.md)** - Dataset overview and statistics
- **[gold/DATA_DICTIONARY.md](gold/DATA_DICTIONARY.md)** - Complete schema with column types and descriptions

## 🔑 Key Features

### Data Quality
✅ Realistic, interconnected data with proper referential integrity  
✅ Deterministic generation with seeded random values for reproducibility  
✅ Fraud flags for fraud detection analysis (~2-3% simulated fraud rate)  
✅ Temporal data spanning full year with realistic patterns  

### Tables & Relationships

```
CUSTOMERS (500)
    ├── has many ─> CARDS (820)
    │                └── used in ──> TRANSACTIONS (5,000)
    │                                    ├── to ──> MERCHANTS (200)
    │                                    └── summarized in ──> CUSTOMER_SPENDING_SUMMARY (500)
    │                                                           └── MERCHANT_PERFORMANCE_SUMMARY (200)
    │
    └── TIME_SERIES: DAILY_TRANSACTIONS_SUMMARY (365)
```

### Data Coverage

| Metric | Value |
|--------|-------|
| Active Customers | 500 |
| Total Cards | 820 |
| Unique Merchants | 200 |
| Total Transactions | 5,000 |
| Transaction Amount Range | $0.50 - $999.99 |
| Date Coverage | 365 days (1 full year) |
| Fraud Records | ~130 (2.6% fraud rate) |

## 💡 Use Cases

### Analytics & BI
- Customer segmentation analysis
- Merchant category performance
- Daily transaction trend analysis
- Customer lifetime value (CLV) calculations

### Data Science
- Fraud detection model training
- Customer spending pattern analysis
- Churn prediction modeling
- Merchant clustering

### Testing & Validation
- Data pipeline testing
- ETL validation
- BI tool demonstrations
- Database schema validation

## 🔒 About the Data

This is **100% synthetic data** generated using the Faker library:
- No real customer information
- Random but realistic patterns
- Perfect for testing and education
- Fully reproducible (seeded generation)

## 📝 Customization

To modify dataset parameters, edit `generate_card_data.py`:

```python
NUM_CUSTOMERS = 500              # Change number of customers
NUM_CARDS_PER_CUSTOMER = 1.5    # Average cards per customer
NUM_MERCHANTS = 200              # Change number of merchants
NUM_TRANSACTIONS = 5000          # Change transaction count
```

Then regenerate:
```bash
python generate_card_data.py
```

## 📚 Data Schema Highlights

### Key Tables

**CUSTOMERS**: Core customer dimension
- Customer IDs: `CUST_000001` to `CUST_000500`
- Segments: Premium, Standard, Basic
- Status: Active, Inactive

**CARDS**: Payment card dimension
- Card IDs: `CARD_00000001` to `CARD_00000820`
- Brands: Visa, Mastercard, American Express, Discover
- Types: Credit, Debit, Business

**MERCHANTS**: Merchant dimension
- Merchant IDs: `MERCH_000001` to `MERCH_000200`
- 15 Categories: Grocery, Gas, Restaurant, Hotel, Airlines, Retail, Entertainment, Utilities, Healthcare, Online Shopping, Subscription, Automotive, Pharmacy, Coffee Shop, Gym

**TRANSACTIONS**: Complete transaction log
- Transaction IDs: `TXN_000000001` to `TXN_000005000`
- Status: Completed (~95%), Declined (~3%), Pending (~2%)
- Includes fraud flags for ML training

## 🛠️ Technical Details

- **Language**: Python 3.8+
- **Libraries**: pandas, numpy, faker
- **Output Format**: CSV
- **CSV Encoding**: UTF-8
- **Timestamp Format**: YYYY-MM-DD HH:MM:SS UTC
- **Reproducibility**: Seeded random generation (numpy.seed(42), Faker.seed(42))

## 📧 Support

For issues, questions, or suggestions, please refer to the detailed documentation in:
- [gold/README.md](gold/README.md)
- [gold/DATA_DICTIONARY.md](gold/DATA_DICTIONARY.md)

---

**Last Updated**: March 25, 2026  
**Dataset Version**: 1.0  
**Status**: Production Ready
