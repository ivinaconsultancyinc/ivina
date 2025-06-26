import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

def simulate_mortality_lapse_data():
    np.random.seed(42)
    dates = pd.date_range(start='2015-01-01', periods=365*5, freq='D')
    age = np.random.randint(18, 70, size=len(dates))
    policy_duration = np.random.randint(1, 30, size=len(dates))
    mortality = np.random.binomial(1, 0.01, size=len(dates))
    lapse = np.random.binomial(1, 0.05, size=len(dates))
    data = pd.DataFrame({'ds': dates, 'age': age, 'policy_duration': policy_duration, 'mortality': mortality, 'lapse': lapse})
    return data

def train_mortality_model(data):
    X_mortality = data[['age', 'policy_duration']]
    y_mortality = data['mortality']
    mortality_model = LogisticRegression()
    mortality_model.fit(X_mortality, y_mortality)
    return mortality_model

def train_lapse_model(data):
    X_lapse = data[['age', 'policy_duration']]
    y_lapse = data['lapse']
    lapse_model = LogisticRegression()
    lapse_model.fit(X_lapse, y_lapse)
    return lapse_model

def predict_mortality_lapse(data, mortality_model, lapse_model):
    X_mortality = data[['age', 'policy_duration']]
    X_lapse = data[['age', 'policy_duration']]
    data['mortality_pred'] = mortality_model.predict_proba(X_mortality)[:, 1]
    data['lapse_pred'] = lapse_model.predict_proba(X_lapse)[:, 1]
    return data

def plot_mortality_lapse(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data['ds'], data['mortality_pred'], label='Mortality Prediction')
    plt.plot(data['ds'], data['lapse_pred'], label='Lapse Prediction')
    plt.title('Mortality and Lapse Predictions Over Time')
    plt.xlabel('Date')
    plt.ylabel('Probability')
    plt.legend()
    plt.show()
