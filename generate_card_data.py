import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os

# Set seed for reproducibility
np.random.seed(42)
Faker.seed(42)
fake = Faker()

# Configuration
NUM_CUSTOMERS = 500
NUM_CARDS_PER_CUSTOMER = 1.5
NUM_MERCHANTS = 200
NUM_TRANSACTIONS = 5000

# Create output directory
output_dir = 'gold'
os.makedirs(output_dir, exist_ok=True)

print("Generating synthetic card dataset for gold layer...\n")

# ============================================================================
# 1. CUSTOMERS TABLE
# ============================================================================
print("Generating customers...")
customers = []
for i in range(NUM_CUSTOMERS):
    customer_id = f"CUST_{i+1:06d}"
    customers.append({
        'customer_id': customer_id,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80),
        'address': fake.address().replace('\n', ', '),
        'city': fake.city(),
        'state': fake.state(),
        'zip_code': fake.zipcode(),
        'country': 'US',
        'customer_segment': np.random.choice(['Premium', 'Standard', 'Basic']),
        'account_status': np.random.choice(['Active', 'Active', 'Active', 'Inactive']),
        'account_open_date': fake.date_between(start_date='-5y'),
        'created_at': datetime.now()
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv(os.path.join(output_dir, 'customers.csv'), index=False)
print(f"✓ Created customers.csv ({len(customers_df)} rows)\n")

# ============================================================================
# 2. CARDS TABLE
# ============================================================================
print("Generating cards...")
cards = []
card_types = ['Credit', 'Debit', 'Business']
card_brands = ['Visa', 'Mastercard', 'American Express', 'Discover']

for customer_id in customers_df['customer_id']:
    num_cards = np.random.choice([1, 2, 3], p=[0.5, 0.35, 0.15])
    for j in range(num_cards):
        card_id = f"CARD_{len(cards)+1:08d}"
        card_number = ''.join([str(np.random.randint(0, 10)) for _ in range(16)])
        expiry_month = np.random.randint(1, 13)
        expiry_year = np.random.randint(2025, 2032)
        
        cards.append({
            'card_id': card_id,
            'customer_id': customer_id,
            'card_brand': np.random.choice(card_brands),
            'card_type': np.random.choice(card_types),
            'card_number_last_4': card_number[-4:],
            'card_number_hash': f"hash_{card_number}",
            'cardholder_name': customers_df[customers_df['customer_id'] == customer_id]['first_name'].values[0] + ' ' + 
                              customers_df[customers_df['customer_id'] == customer_id]['last_name'].values[0],
            'expiry_month': expiry_month,
            'expiry_year': expiry_year,
            'is_default': (j == 0),  # First card is default
            'card_status': np.random.choice(['Active', 'Active', 'Active', 'Blocked', 'Expired']),
            'issued_date': fake.date_between(start_date='-4y'),
            'created_at': datetime.now()
        })

cards_df = pd.DataFrame(cards)
cards_df.to_csv(os.path.join(output_dir, 'cards.csv'), index=False)
print(f"✓ Created cards.csv ({len(cards_df)} rows)\n")

# ============================================================================
# 3. MERCHANTS TABLE
# ============================================================================
print("Generating merchants...")
merchants = []
merchant_categories = [
    'Grocery', 'Gas Station', 'Restaurant', 'Hotel', 'Airlines', 'Retail',
    'Entertainment', 'Utilities', 'Healthcare', 'Online Shopping', 'Subscription',
    'Automotive', 'Pharmacy', 'Coffee Shop', 'Gym'
]

for i in range(NUM_MERCHANTS):
    merchant_id = f"MERCH_{i+1:06d}"
    merchants.append({
        'merchant_id': merchant_id,
        'merchant_name': fake.company(),
        'merchant_category': np.random.choice(merchant_categories),
        'country': 'US',
        'city': fake.city(),
        'state': fake.state(),
        'merchant_id_industry': f"MCC_{np.random.randint(1000, 9999)}",
        'created_at': datetime.now()
    })

merchants_df = pd.DataFrame(merchants)
merchants_df.to_csv(os.path.join(output_dir, 'merchants.csv'), index=False)
print(f"✓ Created merchants.csv ({len(merchants_df)} rows)\n")

# ============================================================================
# 4. TRANSACTIONS TABLE
# ============================================================================
print("Generating transactions...")
transactions = []
transaction_status = ['Completed', 'Completed', 'Completed', 'Completed', 'Pending', 'Declined']

base_date = datetime.now() - timedelta(days=365)

for i in range(NUM_TRANSACTIONS):
    transaction_id = f"TXN_{i+1:09d}"
    card = cards_df.sample(1).iloc[0]
    merchant = merchants_df.sample(1).iloc[0]
    
    # Generate realistic transaction amounts based on merchant category
    category = merchant['merchant_category']
    if category == 'Gas Station':
        amount = np.random.uniform(30, 80)
    elif category == 'Grocery':
        amount = np.random.uniform(20, 150)
    elif category == 'Restaurant':
        amount = np.random.uniform(15, 200)
    elif category == 'Hotel':
        amount = np.random.uniform(100, 500)
    elif category == 'Airlines':
        amount = np.random.uniform(200, 1500)
    elif category == 'Online Shopping':
        amount = np.random.uniform(10, 300)
    elif category == 'Subscription':
        amount = np.random.uniform(5, 50)
    else:
        amount = np.random.uniform(10, 200)
    
    amount = round(amount, 2)
    
    transaction_datetime = base_date + timedelta(days=np.random.randint(0, 365))
    
    transactions.append({
        'transaction_id': transaction_id,
        'card_id': card['card_id'],
        'customer_id': card['customer_id'],
        'merchant_id': merchant['merchant_id'],
        'merchant_name': merchant['merchant_name'],
        'merchant_category': merchant['merchant_category'],
        'amount': amount,
        'currency': 'USD',
        'transaction_type': np.random.choice(['Purchase', 'Withdrawal', 'Transfer'], p=[0.85, 0.1, 0.05]),
        'transaction_status': np.random.choice(transaction_status),
        'transaction_date': transaction_datetime.date(),
        'transaction_time': transaction_datetime.time(),
        'transaction_timestamp': transaction_datetime,
        'mcc_code': merchant['merchant_id_industry'],
        'is_fraud': np.random.choice([False, False, False, False, False, True]),  # 1/6 fraud rate for synthetic data
        'created_at': datetime.now()
    })

transactions_df = pd.DataFrame(transactions)
transactions_df.to_csv(os.path.join(output_dir, 'transactions.csv'), index=False)
print(f"✓ Created transactions.csv ({len(transactions_df)} rows)\n")

# ============================================================================
# 5. CUSTOMER SPENDING SUMMARY (Aggregated for Analytics)
# ============================================================================
print("Generating customer spending summary...")
spending_summary = []

for customer_id in customers_df['customer_id']:
    customer_txns = transactions_df[transactions_df['customer_id'] == customer_id]
    customer_cards = cards_df[cards_df['customer_id'] == customer_id]
    
    spending_summary.append({
        'customer_id': customer_id,
        'total_transactions': len(customer_txns),
        'total_spending': customer_txns['amount'].sum(),
        'average_transaction_amount': customer_txns['amount'].mean() if len(customer_txns) > 0 else 0,
        'max_transaction_amount': customer_txns['amount'].max() if len(customer_txns) > 0 else 0,
        'active_cards': len(customer_cards[customer_cards['card_status'] == 'Active']),
        'total_cards': len(customer_cards),
        'fraud_transactions': len(customer_txns[customer_txns['is_fraud'] == True]),
        'fraud_rate': (customer_txns['is_fraud'].sum() / len(customer_txns)) if len(customer_txns) > 0 else 0,
        'last_transaction_date': customer_txns['transaction_date'].max() if len(customer_txns) > 0 else None,
        'days_since_last_transaction': (datetime.now().date() - customer_txns['transaction_date'].max()).days if len(customer_txns) > 0 else None,
        'created_at': datetime.now()
    })

spending_summary_df = pd.DataFrame(spending_summary)
spending_summary_df.to_csv(os.path.join(output_dir, 'customer_spending_summary.csv'), index=False)
print(f"✓ Created customer_spending_summary.csv ({len(spending_summary_df)} rows)\n")

# ============================================================================
# 6. MERCHANT PERFORMANCE SUMMARY (Aggregated for Analytics)
# ============================================================================
print("Generating merchant performance summary...")
merchant_summary = []

for merchant_id in merchants_df['merchant_id']:
    merchant_txns = transactions_df[transactions_df['merchant_id'] == merchant_id]
    
    merchant_summary.append({
        'merchant_id': merchant_id,
        'merchant_name': merchants_df[merchants_df['merchant_id'] == merchant_id]['merchant_name'].values[0],
        'merchant_category': merchants_df[merchants_df['merchant_id'] == merchant_id]['merchant_category'].values[0],
        'total_transactions': len(merchant_txns),
        'total_volume': merchant_txns['amount'].sum(),
        'average_transaction_amount': merchant_txns['amount'].mean() if len(merchant_txns) > 0 else 0,
        'total_customers': merchant_txns['customer_id'].nunique() if len(merchant_txns) > 0 else 0,
        'fraud_transactions': len(merchant_txns[merchant_txns['is_fraud'] == True]),
        'fraud_rate': (merchant_txns['is_fraud'].sum() / len(merchant_txns)) if len(merchant_txns) > 0 else 0,
        'created_at': datetime.now()
    })

merchant_summary_df = pd.DataFrame(merchant_summary)
merchant_summary_df.to_csv(os.path.join(output_dir, 'merchant_performance_summary.csv'), index=False)
print(f"✓ Created merchant_performance_summary.csv ({len(merchant_summary_df)} rows)\n")

# ============================================================================
# 7. DAILY TRANSACTIONS SUMMARY (Time Series for Analytics)
# ============================================================================
print("Generating daily transactions summary...")
daily_summary = []

date_range = pd.date_range(
    start=transactions_df['transaction_date'].min(),
    end=transactions_df['transaction_date'].max(),
    freq='D'
)

for date in date_range:
    day_txns = transactions_df[transactions_df['transaction_date'] == date.date()]
    if len(day_txns) > 0:
        daily_summary.append({
            'date': date.date(),
            'total_transactions': len(day_txns),
            'total_volume': day_txns['amount'].sum(),
            'average_transaction_amount': day_txns['amount'].mean(),
            'unique_customers': day_txns['customer_id'].nunique(),
            'unique_merchants': day_txns['merchant_id'].nunique(),
            'fraud_transactions': len(day_txns[day_txns['is_fraud'] == True]),
            'fraud_rate': (day_txns['is_fraud'].sum() / len(day_txns)) if len(day_txns) > 0 else 0,
        })

daily_summary_df = pd.DataFrame(daily_summary)
daily_summary_df.to_csv(os.path.join(output_dir, 'daily_transactions_summary.csv'), index=False)
print(f"✓ Created daily_transactions_summary.csv ({len(daily_summary_df)} rows)\n")

# ============================================================================
# SUMMARY REPORT
# ============================================================================
print("="*70)
print("DATASET GENERATION COMPLETE")
print("="*70)
print(f"\nGold Layer Tables Generated:")
print(f"  • customers.csv                    - {len(customers_df):>6} rows")
print(f"  • cards.csv                        - {len(cards_df):>6} rows")
print(f"  • merchants.csv                    - {len(merchants_df):>6} rows")
print(f"  • transactions.csv                 - {len(transactions_df):>6} rows")
print(f"  • customer_spending_summary.csv    - {len(spending_summary_df):>6} rows")
print(f"  • merchant_performance_summary.csv - {len(merchant_summary_df):>6} rows")
print(f"  • daily_transactions_summary.csv   - {len(daily_summary_df):>6} rows")
print(f"\nTotal Records: {len(customers_df) + len(cards_df) + len(merchants_df) + len(transactions_df) + len(spending_summary_df) + len(merchant_summary_df) + len(daily_summary_df):,}")
print(f"\nOutput Location: {os.path.abspath(output_dir)}")
print(f"\nData Quality Metrics:")
print(f"  • Transaction Date Range: {transactions_df['transaction_date'].min()} to {transactions_df['transaction_date'].max()}")
print(f"  • Total Transaction Volume: ${transactions_df['amount'].sum():,.2f}")
print(f"  • Fraud Rate: {(transactions_df['is_fraud'].sum() / len(transactions_df) * 100):.2f}%")
print(f"  • Active Customer Accounts: {len(customers_df[customers_df['account_status'] == 'Active'])}")
print("="*70)
