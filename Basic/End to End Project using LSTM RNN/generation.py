# synthetic_data_generator.py
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

n_rows = 5000

# Generate realistic synthetic data
data = {
    'customer_id': range(1, n_rows + 1),
    'age': np.random.normal(35, 12, n_rows).astype(int),
    'annual_income': np.random.lognormal(mean=10.5, sigma=0.8, size=n_rows),
    'spending_score': np.random.beta(2, 5, n_rows) * 100,
    'days_since_last_purchase': np.random.exponential(scale=60, size=n_rows),
    'credit_score': np.random.normal(650, 80, n_rows),
    'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_rows),
    'signup_date': [datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1825)) for _ in range(n_rows)]
}

df = pd.DataFrame(data)

# Round numeric columns
df['annual_income'] = df['annual_income'].round(2)
df['spending_score'] = df['spending_score'].round(1)
df['days_since_last_purchase'] = df['days_since_last_purchase'].round(1)
df['credit_score'] = df['credit_score'].round(0).astype(int)

# Introduce realistic constraints
df['age'] = df['age'].clip(18, 80)
df['credit_score'] = df['credit_score'].clip(300, 850)

# Introduce OUTLIERS (extreme but plausible)
outlier_mask = np.random.choice(df.index, size=80, replace=False)
df.loc[outlier_mask[:40], 'annual_income'] *= np.random.uniform(5, 15, 40)  # Super rich
df.loc[outlier_mask[40:60], 'annual_income'] = df.loc[outlier_mask[40:60], 'annual_income'] * 0.05  # Very poor
df.loc[outlier_mask[60:], 'spending_score'] = np.random.uniform(95, 100, 20)

# Introduce MISSING VALUES (different patterns)
# MCAR: completely random
mcar_cols = ['age', 'spending_score', 'credit_score']
for col in mcar_cols:
    df.loc[df.sample(frac=0.08).index, col] = np.nan

# MAR: missing age more often for low-income people
low_income = df['annual_income'] < df['annual_income'].quantile(0.2)
df.loc[low_income.sample(frac=0.4).index, 'age'] = np.nan

# MNAR: high spenders hide their income
high_spenders = df['spending_score'] > 90
df.loc[high_spenders.sample(frac=0.7).index, 'annual_income'] = np.nan

# Some missing region
df.loc[df.sample(frac=0.05).index, 'region'] = np.nan

# Save raw synthetic data
df.to_csv('raw_synthetic_customers.csv', index=False)
print("Synthetic data generated: raw_synthetic_customers.csv")
print(f"Shape: {df.shape}")
print(f"Missing values:\n{df.isnull().sum()}")