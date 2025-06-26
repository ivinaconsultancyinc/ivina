import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt

def simulate_historical_policy_data():
    np.random.seed(42)
    dates = pd.date_range(start='2015-01-01', periods=365*5, freq='D')
    cash_flows = np.random.poisson(lam=100, size=len(dates))
    data = pd.DataFrame({'ds': dates, 'y': cash_flows})
    return data

def forecast_cash_flows(data):
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)
    return model, forecast

def plot_forecast(model, forecast):
    model.plot(forecast)
    plt.title('Forecast of Future Policy Cash Flows')
    plt.xlabel('Date')
    plt.ylabel('Cash Flow')
    plt.show()

def forecast_claims(data):
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)
    return model, forecast

def plot_claims_forecast(model, forecast):
    model.plot(forecast)
    plt.title('Forecast of Future Insurance Claims')
    plt.xlabel('Date')
    plt.ylabel('Number of Claims')
    plt.show()
