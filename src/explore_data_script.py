import pandas as pd
import os

path = r'C:\Users\leola\Desktop\Projet smartEngine\data\raw'
files = [
    'ravenstack_accounts.csv',
    'ravenstack_churn_events.csv',
    'ravenstack_feature_usage.csv',
    'ravenstack_subscriptions.csv',
    'ravenstack_support_tickets.csv'
]

results = ""

for f in files:
    file_path = os.path.join(path, f)
    if not os.path.exists(file_path):
        results += f"File {f} not found.\n"
        continue
    
    df = pd.read_csv(file_path)
    results += f"--- {f} ---\n"
    results += f"Shape: {df.shape}\n"
    results += f"Columns: {list(df.columns)}\n"
    results += f"Types:\n{df.dtypes}\n"
    results += f"Missing values:\n{df.isnull().sum()}\n"
    results += f"Head:\n{df.head().to_string()}\n"
    results += "\n"

print(results)
