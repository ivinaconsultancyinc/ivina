import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def simulate_economic_scenarios():
    np.random.seed(42)
    dates = pd.date_range(start='2015-01-01', periods=365*5, freq='D')
    interest_rates = np.random.normal(loc=0.03, scale=0.01, size=len(dates))
    equity_returns = np.random.normal(loc=0.07, scale=0.15, size=len(dates))
    data = pd.DataFrame({'ds': dates, 'interest_rates': interest_rates, 'equity_returns': equity_returns})
    return data

def plot_economic_scenarios(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['ds'], data['interest_rates'], label='Interest Rates')
    plt.plot(data['ds'], data['equity_returns'], label='Equity Returns')
    plt.title('Simulated Economic Scenarios')
    plt.xlabel('Date')
    plt.ylabel('Rate/Return')
    plt.legend()
    plt.show()
