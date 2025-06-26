import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def simulate_policy_data():
    np.random.seed(42)
    dates = pd.date_range(start='2015-01-01', periods=365*5, freq='D')
    cash_flows = np.random.poisson(lam=100, size=len(dates))
    return dates, cash_flows

def calculate_reserves(dates, cash_flows, discount_rate):
    reserves = np.zeros(len(dates))
    for i in range(len(dates)):
        reserves[i] = np.sum(cash_flows[i:] / (1 + discount_rate)**np.arange(1, len(dates)-i+1))
    return reserves

def plot_reserves(dates, reserves):
    plt.figure(figsize=(10, 6))
    plt.plot(dates, reserves, label='Reserves')
    plt.title('Policy Reserves Over Time')
    plt.xlabel('Date')
    plt.ylabel('Reserve Amount')
    plt.legend()
    plt.show()
