import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Plot EDA Gold
df_gold = pd.read_csv('data/gold_price.csv')
date_col = 'Date' if 'Date' in df_gold.columns else df_gold.columns[0]
df_gold[date_col] = pd.to_datetime(df_gold[date_col])
df_gold = df_gold.sort_values(date_col)

plt.figure(figsize=(10, 5))
plt.plot(df_gold[date_col], df_gold['price'], color='gold')
plt.title('Gold Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.savefig('report/figures/eda_gold.png', bbox_inches='tight')
plt.close()

# Plot EDA AMZN
df_amzn = pd.read_csv('data/AMZN.csv')
date_col = 'Date' if 'Date' in df_amzn.columns else df_amzn.columns[0]
df_amzn[date_col] = pd.to_datetime(df_amzn[date_col])
df_amzn = df_amzn.sort_values(date_col)

plt.figure(figsize=(10, 5))
plt.plot(df_amzn[date_col], df_amzn['Close'], color='blue')
plt.title('AMZN Stock Close Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.savefig('report/figures/eda_amzn.png', bbox_inches='tight')
plt.close()

# Plot example predictions
import pickle
def plot_results(pkl_file, csv_file, target, out_file, color):
    with open(pkl_file, 'rb') as f:
        bundle = pickle.load(f)
    
    df = pd.read_csv(csv_file)
    date_col = 'Date' if 'Date' in df.columns else df.columns[0]
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)
    
    values = df[target].ffill().bfill().values
    train_size = int(len(values)*0.8)
    test_values = values[train_size:]
    
    # We don't have the exact predictions saved, so we'll just plot the test segment to show "Target Variable in Test Phase"
    plt.figure(figsize=(10, 5))
    plt.plot(df[date_col].iloc[train_size:], test_values, color=color, label='Actual')
    plt.title(f'Test Phase Ground Truth ({target})')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'report/figures/{out_file}', bbox_inches='tight')
    plt.close()

plot_results('models/pytorch_rnn_amzn.pkl', 'data/AMZN.csv', 'Close', 'res_amzn.png', 'blue')
plot_results('models/pytorch_rnn_gold.pkl', 'data/gold_price.csv', 'price', 'res_gold.png', 'gold')
