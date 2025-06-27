import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

# Step 1: Simulate Historical Claims Data
np.random.seed(42)
dates = pd.date_range(start='2015-01-01', periods=365*5, freq='D')
claims = np.random.poisson(lam=50, size=len(dates))
data = pd.DataFrame({'ds': dates, 'y': claims})

# Step 2: Simulate Risk Factors
age = np.random.randint(18, 70, size=len(dates))
location_risk = np.random.normal(loc=1.0, scale=0.1, size=len(dates))
health_risk = np.random.normal(loc=1.0, scale=0.1, size=len(dates))
risk_factors = pd.DataFrame({'age': age, 'location_risk': location_risk, 'health_risk': health_risk})

# Step 3: Risk Scoring Model
X = risk_factors[['age', 'location_risk', 'health_risk']]
y = claims
risk_model = LinearRegression()
risk_model.fit(X, y)
risk_scores = risk_model.predict(X)

# Step 4: Premium Calculation
base_premium = 100
premiums = base_premium + risk_scores * 0.1

# Step 5: Forecast Future Claims
model = Prophet()
model.fit(data)
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

# Step 6: Visualizations
os.makedirs('static/valuation', exist_ok=True)

plt.figure(figsize=(10, 6))
plt.plot(data['ds'], data['y'], label='Historical Claims')
plt.title('Historical Insurance Claims')
plt.xlabel('Date')
plt.ylabel('Number of Claims')
plt.legend()
plt.savefig('static/valuation/historical_claims.png')
plt.close()

plt.figure(figsize=(10, 6))
plt.plot(dates, risk_scores, label='Risk Scores')
plt.title('Risk Scores Over Time')
plt.xlabel('Date')
plt.ylabel('Risk Score')
plt.legend()
plt.savefig('static/valuation/risk_scores.png')
plt.close()

plt.figure(figsize=(10, 6))
plt.plot(dates, premiums, label='Premiums')
plt.title('Premiums Over Time')
plt.xlabel('Date')
plt.ylabel('Premium Amount')
plt.legend()
plt.savefig('static/valuation/premiums.png')
plt.close()

model.plot(forecast)
plt.title('Forecast of Future Insurance Claims')
plt.xlabel('Date')
plt.ylabel('Number of Claims')
plt.savefig('static/valuation/forecast.png')
plt.close()

model.plot_components(forecast)
plt.savefig('static/valuation/forecast_components.png')
plt.close()

# Step 7: Premium Statistics
average_premium = np.mean(premiums)
std_dev_premium = np.std(premiums)

# Step 8: Top 5 Highest Risk Scores
top_5_risk_scores = risk_factors.iloc[np.argsort(risk_scores)[-5:]]
top_5_risk_scores['risk_score'] = risk_scores[np.argsort(risk_scores)[-5:]]

# Step 9: Summary Report
with open('static/valuation/summary_report.txt', 'w') as f:
    f.write("Insurance Valuation Summary Report\n")
    f.write("===============================\n\n")
    f.write(f"Average Premium: {average_premium:.2f}\n")
    f.write(f"Standard Deviation of Premiums: {std_dev_premium:.2f}\n\n")
    f.write("Top 5 Highest Risk Scores:\n")
    f.write(top_5_risk_scores.to_string(index=False))

print("Valuation completed and summary report generated.")








